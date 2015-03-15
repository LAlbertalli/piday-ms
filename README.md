# Happy PiDay with millisecond precision
### Tweet on PiDay with millisecond precision
![equation](http://www.sciweavers.org/tex2img.php?eq=%20%5Cpi%20%3D%204%20%2A%20%5Csum%5Climits_%7Bn%3D0%7D%5E%5Cinfty%20%20%5Cfrac%7B%28-1%29%5En%7D%7B2%2An%2B1%7D%20&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=0)

Four time the sum of minus one at the power of n over two times n plus 1 for n going from zero to infinite

This programs has been designed to send an Happy PiDay Tweet on 3/14/15 at 9:26:53.590 UTC with millisecond precision as described [here](https://medium.com/@albluca/happy-pi-day-tweeted-with-millisecond-precision-338c4f68afc3).

## Program Usage
### Requirements

The code is written in python2 and has been used on Python 2.7.3. I cannot guarantee that it works on other version of Python. The programs requirements are only [Tweepy](https://github.com/tweepy/tweepy) version 3.0 or better and [Requests](http://docs.python-requests.org/en/latest/).

For the data analysis part also [SciKit Learn](http://scikit-learn.org/stable/) is required.

# sp80.py
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
                        Index in the message_set list to be used for the
                        tweets
  -r, --run             Do the actual tweet
  -c, --calibrate       Calibrate the Twitter
  -t TARGET, --target TARGET
                        Time to tweet
```
