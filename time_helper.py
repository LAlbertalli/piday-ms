import time
from datetime import datetime, timedelta

def launch_at(when,func,*args,**kwargs):
    target = time.mktime(when.timetuple())+.000001*when.microsecond
    now = time.time()
    if target - now < 1:
        raise Exception("Too late")
    while target - now > 3:
        diff = min(target - now - 2.5, 60)
        time.sleep(diff)
        now = time.time()
    while target - now > .000001*launch_at.calibration:
        now = time.time()
    func(*args,**kwargs)
launch_at.calibration = 1

def calibrate(rounds=10, delay = 3, change = True):
    delays = []
    def test(when):
        now = datetime.now()
        delays.append((now,when))
    for i in xrange(rounds):
        print("Calibrating round %d"%i)
        when = datetime.now() + timedelta(seconds = delay)
        launch_at(when, test, when)
        print("Round %d Done"%i)
    diffs = [(i-j).total_seconds() for i,j in delays]
    diffs.sort()
    # remove outliers
    l = len(diffs)/2+1
    avg = abs(sum(diffs[:l])/l)
    diffs = filter(lambda x:-3*avg<x<3*avg,diffs)
    
    avg = sum(diffs)/len(diffs)
    std = (sum((i-avg) ** 2 for i in diffs)/len(diffs)) ** 0.5
    if change:
        launch_at.calibration += avg/.000001
    print("Average: %6f ms, Standard Deviation: %6f ms"%(avg * 1000,std * 1000))
    print("Raw data: %s"%diffs)