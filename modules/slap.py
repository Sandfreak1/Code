#!/usr/bin/env python
"""
Stan-Derp Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
slap.py - Stan-Derp slap module
http://standerp.liamstanley.net/
"""


import random

def slap(standerp, input):
    """.slap <target> - Slaps <target>"""
    text = input.group().split()
    if len(text) < 2 or text[1].startswith('#'): return
    if text[1] == standerp.nick:
        if (input.nick not in standerp.config.admins):
            text[1] = input.nick
        else: text[1] = 'himself'
    if text[1] in standerp.config.admins:
        if (input.nick not in standerp.config.admins):
            text[1] = input.nick
    verb = random.choice(('slaps', 'kicks', 'destroys', 'annihilates', 'punches', 'roundhouse kicks', 'rusty hooks', 'pwns', 'owns', 'karate chops', 'kills', 'disintegrates', 'demolishes', 'Pulverizes'))
    afterfact = random.choice(('till they die', 'till they leave the channel', 'till they choke on bitter defeat', 'till they crawl in a hole and die', 'till they disintegrate into mid air', 'into a pancake'))
    standerp.write(['PRIVMSG', input.sender, ' :\x01ACTION', verb, text[1], afterfact, '\x01'])
slap.commands = ['slap']
slap.priority = 'medium'
slap.rate = 60

if __name__ == '__main__':
    print __doc__.strip()