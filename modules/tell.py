#!/usr/bin/env python
"""
Stan-Derp Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
tell.py - Stan-Derp tell Module
http://standerp.liamstanley.net/
"""

import os, re, time, random
import web

maximum = 4
lispchannels = frozenset([ '#lisp', '#scheme', '#opendarwin', '#macdev',
'#fink', '#jedit', '#dylan', '#emacs', '#xemacs', '#colloquy', '#adium',
'#growl', '#chicken', '#quicksilver', '#svn', '#slate', '#squeak', '#wiki',
'#nebula', '#myko', '#lisppaste', '#pearpc', '#fpc', '#hprog',
'#concatenative', '#slate-users', '#swhack', '#ud', '#t', '#compilers',
'#erights', '#esp', '#scsh', '#sisc', '#haskell', '#rhype', '#sicp', '#darcs',
'#hardcider', '#lisp-it', '#webkit', '#launchd', '#mudwalker', '#darwinports',
'#muse', '#chatkit', '#kowaleba', '#vectorprogramming', '#opensolaris',
'#oscar-cluster', '#ledger', '#cairo', '#idevgames', '#hug-bunny', '##parsers',
'#perl6', '#sdlperl', '#ksvg', '#rcirc', '#code4lib', '#linux-quebec',
'#programmering', '#maxima', '#robin', '##concurrency', '#paredit' ])

def loadReminders(fn):
    result = {}
    f = open(fn)
    for line in f:
        line = line.strip()
        if line:
            try: tellee, teller, verb, timenow, msg = line.split('\t', 4)
            except ValueError: continue
            result.setdefault(tellee, []).append((teller, verb, timenow, msg))
    f.close()
    return result

def dumpReminders(fn, data):
    f = open(fn, 'w')
    for tellee in data.iterkeys():
        for remindon in data[tellee]:
            line = '\t'.join((tellee,) + remindon)
            try: f.write(line + '\n')
            except IOError: break
    try: f.close()
    except IOError: pass
    return True

def setup(self):
    fn = self.nick + '-' + self.config.host + '.tell.db'
    self.tell_filename = os.path.join(os.path.expanduser('~/.standerp'), fn)
    if not os.path.exists(self.tell_filename):
        try: f = open(self.tell_filename, 'w')
        except OSError: pass
        else:
            f.write('')
            f.close()
    self.reminders = loadReminders(self.tell_filename)

def f_remind(standerp, input):
    teller = input.nick

    if input.group() and (input.group()).startswith(".tell"):
        verb = "tell".encode('utf-8')
        line = input.groups()
        line_txt = line[1].split()
        tellee = line_txt[0]
        msg = " ".join(line_txt[1:])
    else:
        verb, tellee, msg = input.groups()
    verb = verb.encode('utf-8')
    tellee = tellee.encode('utf-8')
    msg = msg.encode('utf-8')

    tellee_original = tellee.rstrip('.,:;')
    tellee = tellee_original.lower()

    if not os.path.exists(standerp.tell_filename):
        return

    timenow = time.strftime('%d %b %H:%MZ', time.gmtime())
    whogets = list()
    for tellee in tellee.split(","):
        if len(tellee) > 20:
            standerp.say("Nickname %s is too long." % (tellee))
            continue
        if not tellee in (teller.lower(), standerp.nick, 'me'):
            warn = False
            if not tellee in whogets:
                whogets.append(tellee)
                if tellee not in standerp.reminders:
                    standerp.reminders[tellee] = [(teller, verb, timenow, msg)]
                else:
                    # if len(standerp.reminders[tellee]) >= maximum:
                    #   warn = True
                    standerp.reminders[tellee].append((teller, verb, timenow, msg))
    response = str()
    if teller.lower() == tellee:
        response = 'You can %s yourself that.' % (verb)
    elif tellee.lower() == standerp.nick.lower():
        response = "Hey, I'm not as stupid as Monty you know!"
    else:
        response = "I'll pass that on when %s is around."
        if len(whogets) > 1:
            listing = ", ".join(whogets[:-1]) + " or " + whogets[-1]
            response = response % (listing)
        else:
            response = response % (whogets[0])

    if not whogets:
        rand = random.random()
        if rand > 0.9999: response = "yeah, yeah"
        elif rand > 0.999: response = "yeah, sure, whatever"

    standerp.reply(response)

    dumpReminders(standerp.tell_filename, standerp.reminders)
f_remind.rule = ('$nick', ['[tT]ell', '[aA]sk'], r'(\S+) (.*)')
f_remind.commands = ['tell', 'to']

def getReminders(standerp, channel, key, tellee):
    lines = []
    template = "%s: %s <%s> %s %s %s"
    today = time.strftime('%d %b', time.gmtime())

    for (teller, verb, datetime, msg) in standerp.reminders[key]:
        if datetime.startswith(today):
            datetime = datetime[len(today)+1:]
        lines.append(template % (tellee, datetime, teller, verb, tellee, msg))

    try: del standerp.reminders[key]
    except KeyError: standerp.msg(channel, 'Hmm...')
    return lines

def message(standerp, input):
    if not input.sender.startswith('#'): return

    tellee = input.nick
    channel = input.sender

    if not os: return
    if not os.path.exists(standerp.tell_filename):
        return

    reminders = []
    remkeys = list(reversed(sorted(standerp.reminders.keys())))
    for remkey in remkeys:
        if not remkey.endswith('*') or remkey.endswith(':'):
            if tellee.lower() == remkey:
                reminders.extend(getReminders(standerp, channel, remkey, tellee))
        elif tellee.lower().startswith(remkey.rstrip('*:')):
            reminders.extend(getReminders(standerp, channel, remkey, tellee))

    for line in reminders[:maximum]:
        standerp.say(line)

    if reminders[maximum:]:
        standerp.say('Further messages sent privately')
        for line in reminders[maximum:]:
            standerp.msg(tellee, line)

    if len(standerp.reminders.keys()) != remkeys:
        dumpReminders(standerp.tell_filename, standerp.reminders)
message.rule = r'(.*)'
message.priority = 'low'

if __name__ == '__main__':
    print __doc__.strip()
