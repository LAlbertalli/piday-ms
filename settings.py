settings = {
    'accounts':[
        {
            'api': 'default',
            'token': '<USER ACCESS TOKEN KEY>',
            'secret': '<USER ACCESS TOKEN SECRET>',
        },
    ],
    'apis':{
        'default':{
            'key': '<APP ACCESS TOKEN KEY>',
            'secret': '<APP ACCESS TOKEN SECRET>',
        },
    },
    'target_time': {
        'month': 3,
        'day': 14,
        'year': 2015, #15
        'hour': 9,
        'minute': 26,
        'second': 53,
        'microsecond': 589793,
    },
    'message_set':[
        {
            'target': 'Happy 3/14/15 tweeted with millisec precision! #PiDay',
            'test': 'Test for #PiDay',
            'ramp_up_0': 'First message of the #PiDay #hack',
            'ramp_up_1': 'Getting ready for #PiDay',
            'ramp_up_2': 'Ready to go',
        },
        {
            'target': 'Happy #PiDay - tweeted on 3/14/15 with millisec precision!',
            'test': 'Hacking #PiDay in progress',
            'ramp_up_0': 'Preparing the #PiDay #hack',
            'ramp_up_1': 'We are getting closer #PiDay',
            'ramp_up_2': 'Here we go!!!',
        },
    ],
}