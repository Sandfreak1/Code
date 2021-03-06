#!/usr/bin/env python
# coding=utf-8
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
calc.py - Code Calculator Module
http://code.liamstanley.net/
"""

import re
import web
import unicodedata

r_result = re.compile(r'(?i)<A NAME=results>(.*?)</A>')
r_tag = re.compile(r'<\S+.*?>')

subs = [
   (' in ', ' -> '), 
   (' over ', ' / '), 
   (u'£', 'GBP '), 
   (u'€', 'EUR '), 
   ('\$', 'USD '), 
   (r'\bKB\b', 'kilobytes'), 
   (r'\bMB\b', 'megabytes'), 
   (r'\bGB\b', 'kilobytes'), 
   ('kbps', '(kilobits / second)'), 
   ('mbps', '(megabits / second)')
]

def dcalc(code, input): 
   """Frink Online Calculator"""
   q = input.group(2)
   if not q: 
      return code.say('0?')

   query = q[:]
   for a, b in subs: 
      query = re.sub(a, b, query)
   query = query.rstrip(' \t')

   precision = 5
   if query[-3:] in ('GBP', 'USD', 'EUR', 'NOK'): 
      precision = 2
   query = web.urllib.quote(query.encode('utf-8'))

   uri = 'http://futureboy.us/fsp/frink.fsp?fromVal='
   bytes = web.get(uri + query)
   m = r_result.search(bytes)
   if m: 
      result = m.group(1)
      result = r_tag.sub('', result) # strip span.warning tags
      result = result.replace('&gt;', '>')
      result = result.replace('(undefined symbol)', '(?) ')

      if '.' in result: 
         try: result = str(round(float(result), precision))
         except ValueError: pass

      if not result.strip(): 
         result = '?'
      elif ' in ' in q: 
         result += ' ' + q.split(' in ', 1)[1]

      code.say(q + ' = ' + result[:350])
   else: code.reply(code.color('red', 'Sorry, can\'t calculate that.'))
   code.say(code.color('blue', 'Note that .dcalc/.cd is deprecated, consider using .calc'))
dcalc.commands = ['dcalc', 'dc']
dcalc.example = '.dcalc 5 + 3'

def calc(code, input): 
   """Google calculator."""
   if not input.group(2):
      return code.reply(code.color('red', 'Nothing to calculate.'))
   q = input.group(2).encode('utf-8')
   q = q.replace('\xcf\x95', 'phi') # utf-8 U+03D5
   q = q.replace('\xcf\x80', 'pi') # utf-8 U+03C0
   uri = 'http://www.google.com/ig/calculator?q='
   bytes = web.get(uri + web.urllib.quote(q))
   parts = bytes.split('",')
   answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
   if answer: 
      answer = answer.decode('unicode-escape')
      answer = ''.join(chr(ord(c)) for c in answer)
      answer = answer.decode('utf-8')
      answer = answer.replace(u'\xc2\xa0', ',')
      answer = answer.replace('<sup>', '^(')
      answer = answer.replace('</sup>', ')')
      answer = web.decode(answer)
      answer.encode('ascii','ignore')
      #if any(c.isalpha() for c in answer):
      try:
          #firstchar = re.search(r'(\d )+ (.*)',answer)
          fletter = next(i for i, c in enumerate(answer) if c.isalpha())
          number = answer[0:fletter-1]
          words = answer[fletter:len(answer)]
          number.strip()
          cnumb = number.join(number.split())
          words = ' ' + words.strip()
          #[17:02:55] <Avaris> Liam-: next(i for i, c in enumerate(s) if c.isalpha())
          #[17:03:59] <Avaris> (throws StopIteration if there is no letter in the original string)
          code.say(code.bold(cnumb) + code.color('blue', words))
      except:
          answer.strip()
          code.say(answer)
   else: code.say(code.color('red', 'Sorry, no result.'))
calc.commands = ['c', 'calc', 'calculate']
calc.example = '.calc 5 + 3'

def py(code, input):
   if not input.group(2):
       return code.reply('Please enter an %s' % code.bold('input'))
   query = input.group(2).encode('utf-8')
   uri = 'http://tumbolia.appspot.com/py/'
   try:
       answer = web.get(uri + web.urllib.quote(query))
       if answer:
           code.say(answer)
       else:
           code.reply('Sorry, no %s' % code.bold('result'))
   except Exception, e:
       code.reply(code.color('red', 'The server did not return an answer.'))
       print '[.py]', e
py.commands = ['py', 'python']
py.example = '.py print(int(1.0) + int(3))'

def wa(code, input): 
   if not input.group(2):
      return code.reply('No search term.')
   query = input.group(2).encode('utf-8')
   uri = 'http://tumbolia.appspot.com/wa/'
   answer = web.get(uri + web.urllib.quote(query.replace('+', '%2B')))
   if answer: 
      code.say(answer)
   else: code.reply('Sorry, no result.')
wa.commands = ['wa']

if __name__ == '__main__': 
   print __doc__.strip()
