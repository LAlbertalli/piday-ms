# Happy PiDay with millisecond precision
### Tweet on PiDay with millisecond precision
![equation](https://raw.githubusercontent.com/LAlbertalli/piday-ms/master/pi.png)

Four time the sum of minus one at the power of n over two times n plus 1 for n going from zero to infinite

This programs has been designed to send an Happy PiDay Tweet on 3/14/15 at 9:26:53.590 UTC with millisecond precision as described [here](https://medium.com/@albluca/happy-pi-day-tweeted-with-millisecond-precision-338c4f68afc3).

## Program Usage
### Requirements

The code is written in python2 and has been used on Python 2.7.3. I cannot guarantee that it works on other version of Python. The programs requirements are only [Tweepy](https://github.com/tweepy/tweepy) version 3.0 or better and [Requests](http://docs.python-requests.org/en/latest/).

For the data analysis part also [SciKit Learn](http://scikit-learn.org/stable/) is required.

### sp80.py
The main program is in sp80.py:
```shell
python sp80.py -h
usage: sp80.py [-h] [-a ACCOUNT] [-m MESSAGE] (-r | -c) [-t TARGET]
               [calibration]

Secret Project 80/PI. Tweet on "four time the sum of minus one at the power of
n over two times n plus 1 for n going from zero to infinite"

positional arguments:
  calibration           Database with the calibration data

optional arguments:
  -h, --help            show this help message and exit
  -a ACCOUNT, --account ACCOUNT
                        Index in the account list to be used to tweet
  -m MESSAGE, --message MESSAGE
                        Index in the message_set list to be used for the tweets
  -r, --run             Do the actual tweet
  -c, --calibrate       Calibrate the Twitter
  -t TARGET, --target TARGET
                        Time to tweet
```
So ```python sp80.py -c``` will launch the program in calibration mode (send a sequence of 4 tweets immediately deleted to get calibration data) and will store the info in the file ```calibration.db```. Using ```python sp80.py -r``` will run the program in real mode. ```-a``` and ```-m``` select the twitter account and the message set to use, if ignored use the default index = 0. ```-t``` override the target time. The time should be in RFC 2822 format.

**Before running the program check the file ```settings.py```.**
### settings.py
The file ```settings.py``` is the main source of configuration information for ```sp80.py```. It contains a single dict with the following keys:
* ```accounts```: a list of dicts with the accounts to be used to send the tweets
* ```apis``` a list of dicts with api keys for the Twitter app to be used to send the tweets
* ```target_time``` a dict with the target time at which the tweet must be sent
* ```message_set``` a list of dicts with the messages to be used. Each dict should contains the following keys:
  * ```target``` The tweet to be sent on target time
  * ```test``` The tweet sent last in the test sequence. It is used instead of target during calibration
  * ```ramp_up_n``` Sequence of tweets with n going from 0 to 9 (could be less) used during the warming up phase both in calibration and run (in run, if succesfull, are not deleted, so keep them meaningful!)

### data_analysis.py
**TBD**
