#!/usr/bin/env python
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
etymology.py - Code Etymology Module
http://code.liamstanley.net/
"""

import re, urllib
import web
from tools import deprecated

etysite = 'http://www.etymonline.com/index.php?'
etyuri = etysite + 'allowed_in_frame=0&term=%s'
etysearch = etysite + 'allowed_in_frame=0&search=%s'

r_definition = re.compile(r'(?ims)<dd[^>]*>.*?</dd>')
r_tag = re.compile(r'<(?!!)[^>]+>')
r_whitespace = re.compile(r'[\t\r\n ]+')

class Grab(urllib.URLopener): 
   def __init__(self, *args): 
      self.version = 'Mozilla/5.0 (code)'
      urllib.URLopener.__init__(self, *args)
   def http_error_default(self, url, fp, errcode, errmsg, headers): 
      return urllib.addinfourl(fp, [headers, errcode], "http:" + url)

abbrs = [
   'cf', 'lit', 'etc', 'Ger', 'Du', 'Skt', 'Rus', 'Eng', 'Amer.Eng', 'Sp', 
   'Fr', 'N', 'E', 'S', 'W', 'L', 'Gen', 'J.C', 'dial', 'Gk', 
   '19c', '18c', '17c', '16c', 'St', 'Capt', 'obs', 'Jan', 'Feb', 'Mar', 
   'Apr', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'c', 'tr', 'e', 'g'
]
t_sentence = r'^.*?(?<!%s)(?:\.(?= [A-Z0-9]|\Z)|\Z)'
r_sentence = re.compile(t_sentence % ')(?<!'.join(abbrs))

def unescape(s): 
   s = s.replace('&gt;', '>')
   s = s.replace('&lt;', '<')
   s = s.replace('&amp;', '&')
   return s

def text(html): 
   html = r_tag.sub('', html)
   html = r_whitespace.sub(' ', html)
   return unescape(html).strip()

def etymology(word): 
   """Returns the historical information (usually) for a word"""
   
   if len(word) > 25: 
      raise ValueError("Word too long: %s[...]" % word[:10])
   word = {'axe': 'ax/axe'}.get(word, word)

   grab = urllib._urlopener
   urllib._urlopener = Grab()
   urllib._urlopener.addheader("Referer", "http://www.etymonline.com/")
   bytes = web.get(etyuri % web.urllib.quote(word))
   urllib._urlopener = grab
   definitions = r_definition.findall(bytes)

   if not definitions: 
      return None

   defn = text(definitions[0])
   m = r_sentence.match(defn)
   if not m: 
      return None
   sentence = m.group(0)

   # try: 
   #    sentence = unicode(sentence, 'iso-8859-1')
   #    sentence = sentence.encode('utf-8')
   # except: pass
   sentence = web.decode(sentence)

   maxlength = 275
   if len(sentence) > maxlength: 
      sentence = sentence[:maxlength]
      words = sentence[:-5].split(' ')
      words.pop()
      sentence = ' '.join(words) + ' [...]'

   sentence = '"' + sentence.replace('"', "'") + '"'
   return sentence + ' - etymonline.com'

@deprecated
def f_etymology(self, origin, match, args): 
   word = match.group(2)

   try: result = etymology(word.encode('iso-8859-1'))
   except IOError: 
      msg = 'Fuck, Can\'t connect to etymonline.com (%s)' % (etyuri % word)
      self.msg(origin.sender, msg)
      return
   except AttributeError: 
      result = None

   if result is not None: 
      self.msg(origin.sender, result)
   else: 
      uri = etysearch % word
      msg = 'Can\'t find the etymology for "%s". Try %s' % (word, uri)
      self.msg(origin.sender, msg)
# @@ Cf. http://swhack.com/logs/2006-01-04#T01-50-22
f_etymology.rule = (['ety'], r"(.+?)$")
f_etymology.thread = True
f_etymology.priority = 'high'

if __name__=="__main__": 
   import sys
   print etymology(sys.argv[1])
