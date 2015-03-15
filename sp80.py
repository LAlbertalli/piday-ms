from reqhack import tweepy
import time_helper
from settings import settings

import argparse, time, json, cPickle as pickle
from datetime import datetime, timedelta # convert now -> utcnow fromtimestamp utcfromtimestamp
from threading import Lock
from email.utils import parsedate

def get_api(aid = 0):
    user = settings['accounts'][aid]
    api_t = settings['apis'][user['api']]
    auth = tweepy.OAuthHandler(api_t['key'], api_t['secret'])
    auth.set_access_token(user['token'], user['secret'])
    return tweepy.API(auth)

def get_target_time(action = 'run', hint = None):
    hint = parsedate(hint)
    if hint is not None:
        return datetime(*hint[:6])+timedelta(microseconds = 589793) # Add pseudo random microsec
    if action == 'run':
        return datetime(
            month = settings['target_time']['month'],
            day = settings['target_time']['day'],
            year = settings['target_time']['year'],
            hour = settings['target_time']['hour'],
            minute = settings['target_time']['minute'],
            second = settings['target_time']['second'],
            microsecond = settings['target_time']['microsecond']
            )
    elif action == 'calibrate':
        return datetime.now() + timedelta(minutes = 1)
    else:
        return datetime.now()

def get_messages(mid, action = 'run'):
    mset = settings['message_set'][mid]
    ramp_up = filter(lambda x:x.startswith('ramp_up'), mset.iterkeys())
    ramp_up.sort()
    target_m = mset['target'] if action == 'run' else mset['test']
    return [mset[i] for i in ramp_up], target_m

def force_connect(api):
    # do just a fake call to open the connection
    api.me()

def tweet(api, status, when, collect):
    ret = api.update_status(status=status)
    collect.register_tweet_sent(ret.id, when)

def destroy_tweets(api, ids):
    for i in ids:
        try:
            status = api.get_status(id=i)
            status.destroy()
            print("Tweet %d destroied"%i)
        except:
            print("Failed to delete tweet %d"%i)


class DataCollect(object):
    class StreamListener(tweepy.StreamListener):
        def __init__(self, api, collector, stop):
            super(self.__class__,self).__init__(api)
            self.__collector = collector
            self.stop = stop
            

        def on_error(self, status_code):
            print "An error has occurred on the stream %s"%status_code
            return True

        def on_timeout(self):
            pass

        def on_status(self, status):
            tid = status.id
            ts = long(status._json['timestamp_ms'])
            ts_s  = ts/1000
            ts_ms = ts%1000
            timestamp = datetime.fromtimestamp(ts_s) + timedelta(microseconds = ts_ms * 1000)
            self.__collector.register_tweet_rec(tid, timestamp)
            if self.__collector.json_log is not None:
                self.__collector.json_log += json.dumps(status._json)+'\n'
            if status.text == self.stop:
                return False
            else:
                return True

    def __init__(self, api, stop, db,  log_json = True):
        self.__lock = Lock()
        self.__data = {}
        self.db = db
        listener = self.StreamListener(api, self, stop)
        self.__stream, follow = self.__make_stream(api, listener)
        self.__stream.filter(follow=[follow], async = True)
        self.json_log = "" if log_json else None

    def register_tweet_sent(self, tid, timestamp):
        with self.__lock:
            if tid in self.__data:
                self.__data[tid]['sent'] = timestamp
            else:
                self.__data[tid]={
                    'sent': timestamp,
                }

    def register_tweet_rec(self, tid, timestamp):
        with self.__lock:
            if tid in self.__data:
                self.__data[tid]['rec'] = timestamp
            else:
                self.__data[tid]={
                    'rec': timestamp,
                }

    def __make_stream(self, api, listener):
        uid = api.auth.access_token.split('-')[0]
        return tweepy.Stream(api.auth, listener, timeout = None), uid

    def print_data(self):
        print(self.__data)

    def data(self, with_keys = False):
        if with_keys:
            # Get only the data sent by this instance
            data = filter(lambda x:'sent' in x[1], self.__data.items())
            data.sort(key = lambda x:x[1]['sent'])
            return data
        else:
            # Get only the data sent by this instance
            data = filter(lambda x:'sent' in x, self.__data.values())
            data.sort(key = lambda x:x['sent'])
            return data

    def on_target(self):
        data = self.data()[-1]
        return (data['rec'] - data['sent']).total_seconds()

    def get_target_data(self):
        td = self.data(True)
        td.sort(key = lambda x:x[1]['sent'])
        td = td[-1]
        return td[0], td[1]['rec'], td[1]['sent']

    def export_data(self):
        self.db.add_data(self.data())
        if self.json_log:
            with open(datetime.utcnow().strftime("log%m%d%y%H%M%S.json"),"w") as f:
                f.write(self.json_log)

    def predict_delay(self):
        delays = [(i['rec']-i['sent']).total_seconds() for i in self.data()]
        return sum(delays)/len(delays) * 1000000

    def wait(self):
        try:
            self.__stream._thread.join()
        except RuntimeError:
            pass

    def tweet_ids(self):
        return [key for key,value in self.data(True)]

class CalibrationData(object):
    def __init__(self,filename):
        self.__filename = filename
        try:
            with open(self.__filename,"rb") as f:
                self.__data = pickle.load(f)
        except IOError as e:
            if e.errno == 2:
                self.__data = []
            else:
                raise

    def add_data(self,data):
        self.__data += [data]

    def dump(self):
        with open(self.__filename,"wb") as f:
            pickle.dump(self.__data,f)

def main():
    parser = argparse.ArgumentParser(description='Secret Project 80/PI. Tweet on "four time \
the sum of minus one at the power of n over two times n plus 1 for n going from zero \
to infinite"')
    parser.add_argument("-a", "--account", type = int, default = 0, 
        help = "Index in the account list to be used to tweet")
    parser.add_argument("-m", "--message", type = int, default = 0,
        help = "Index in the message_set list to be used for the tweets")
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument("-r", "--run", action = "store_true",
        help = "Do the actual tweet")
    group.add_argument("-c", "--calibrate", action = "store_true",
        help = "Calibrate the Twitter")
    parser.add_argument("-t", "--target", default = None,
        help = "Time to tweet")
    parser.add_argument("calibration", default = "calibration.db", nargs = '?',
        help = "Database with the calibration data")
    args = parser.parse_args()

    print("Calibrate the time_helper. Set 1")
    time_helper.calibrate(rounds = 5, delay = 5)
    print("Calibrate the time_helper. Set 2")
    time_helper.calibrate(rounds = 5)
    print("Calibrate the time_helper. Set 3")
    time_helper.calibrate()
    if args.run:
        when_target = get_target_time("run",args.target)
        ramp_up, m_target = get_messages(args.message, "run")
    elif args.calibrate:
        when_target = get_target_time("calibrate",args.target)
        ramp_up, m_target = get_messages(args.message, "calibrate")

    schedule = [when_target - timedelta(seconds = 2*i + 6) for i in xrange(len(ramp_up)-1, -1, -1)]
    connect_t = schedule[0] - timedelta(seconds = 2)

    api = get_api(args.account)
    db = CalibrationData(args.calibration)
    collector = DataCollect(api,m_target, db)

    def c():
        api.me()
    time_helper.launch_at(connect_t, c)
    
    for i,j in zip(ramp_up, schedule):
        time_helper.launch_at(j,tweet, api, i, j, collector)
    time.sleep(3)
    delay = collector.predict_delay()
    new_target = when_target - timedelta(microseconds = delay)
    print(delay)
    time_helper.launch_at(new_target,tweet, api, m_target, when_target, collector)
    collector.wait()
    on_target = collector.on_target()
    if abs(on_target) < 0.001:
        print("Success!!!")
    print("Tweet sent inside %f s of target time" % on_target)
    print("The tweet %d has been sent at %s, the target was %s"%collector.get_target_data())
    collector.export_data()
    db.dump()
    if args.calibrate or abs(on_target) > 0.001:
        destroy_tweets(api, collector.tweet_ids())

if __name__ == '__main__':
    main()