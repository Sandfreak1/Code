#!/usr/bin/env python
"""
Code Copyright (C) 2012-2013 Liam Stanley
Credits: Sean B. Palmer, Michael Yanovich
head.py - Code HTTP Metadata Utilities
http://code.liamstanley.net/
"""

import re, urllib, urllib2, httplib, urlparse, time
from htmlentitydefs import name2codepoint
import web
from tools import deprecated

def meta(code, input): 
   """Provide HTTP meta (HEAD) information."""
   uri = input.group(2)
   uri = (uri or '').encode('utf-8')
   if ' ' in uri: 
      uri, metaer = uri.rsplit(' ', 1)
   else: uri, metaer = uri, None

   if not uri and hasattr(code, 'last_seen_uri'): 
      try: uri = code.last_seen_uri[input.sender]
      except KeyError: return code.say('?')

   if not uri.startswith('htt'): 
      uri = 'http://' + uri
   # uri = uri.replace('#!', '?_escaped_fragment_=')

   try: info = web.meta(uri)
   except IOError: return code.say("Can't %s to %s" % (code.bold('connect'), uri))
   except httplib.InvalidURL: return code.say("Not a valid URI, sorry.")

   if not isinstance(info, list): 
      try: info = dict(info)
      except TypeError: 
         return code.reply('Try .%s http://example.org/ %s' % (code.color('purple', 'meta'), code.color('blue', '[optional meta]')))
      info['Status'] = '200'
   else: 
      newInfo = dict(info[0])
      newInfo['Status'] = str(info[1])
      info = newInfo

   if metaer is None: 
      data = []
      if info.has_key('Status'): 
         data.append(info['Status'])
      if info.has_key('content-type'): 
         data.append(info['content-type'].replace('; charset=', ', '))
      if info.has_key('last-modified'): 
         modified = info['last-modified']
         modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
         data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
      if info.has_key('content-length'): 
         data.append(info['content-length'] + ' bytes')
      code.reply(', '.join(data))
   else: 
      metaerlower = metaer.lower()
      if info.has_key(metaerlower): 
         code.say(metaer + ': ' + info.get(metaerlower))
      else: 
         msg = 'There was no %s metaer in the response.' % code.bold(metaer)
         code.say(msg)
meta.commands = ['meta']
meta.example = '.meta http://www.w3.org/'

r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
r_entity = re.compile(r'&[A-Za-z0-9#]+;')

@deprecated
def f_title(self, origin, match, args): 
   """.title <URI> - Return the title of URI."""
   uri = match.group(2)
   uri = (uri or '').encode('utf-8')

   if not uri and hasattr(self, 'last_seen_uri'): 
      uri = self.last_seen_uri.get(origin.sender)
   if not uri: 
      return self.msg(origin.sender, 'I need a URI to give the title of...')

   if not ':' in uri: 
      uri = 'http://' + uri
   uri = uri.replace('#!', '?_escaped_fragment_=')

   localhost = [
      'http://localhost/', 'http://localhost:80/', 
      'http://localhost:8080/', 'http://127.0.0.1/', 
      'http://127.0.0.1:80/', 'http://127.0.0.1:8080/', 
      'https://localhost/', 'https://localhost:80/', 
      'https://localhost:8080/', 'https://127.0.0.1/', 
      'https://127.0.0.1:80/', 'https://127.0.0.1:8080/', 
   ]
   for s in localhost: 
      if uri.startswith(s): 
         return code.reply('Sorry, access forbidden.')

   try: 
      redirects = 0
      while True: 
         headers = {
            'Accept': 'text/html', 
            'User-Agent': 'Mozilla/5.0 (code)'
         }
         req = urllib2.Request(uri, headers=headers)
         u = urllib2.urlopen(req)
         info = u.info()
         u.close()
         # info = web.head(uri)

         if not isinstance(info, list): 
            status = '200'
         else: 
            status = str(info[1])
            info = info[0]
         if status.startswith('3'): 
            uri = urlparse.urljoin(uri, info['Location'])
         else: break

         redirects += 1
         if redirects >= 25: 
            self.msg(origin.sender, origin.nick + ": Too many redirects")
            return

      try: mtype = info['content-type']
      except: 
         err = ": Couldn't get the Content-Type, sorry"
         return self.msg(origin.sender, origin.nick + err)
      if not (('/html' in mtype) or ('/xhtml' in mtype)): 
         self.msg(origin.sender, origin.nick + ": Document isn't HTML")
         return

      u = urllib2.urlopen(req)
      bytes = u.read(262144)
      u.close()

   except IOError: 
      self.msg(origin.sender, "Can't connect to %s" % uri)
      return

   m = r_title.search(bytes)
   if m: 
      title = m.group(1)
      title = title.strip()
      title = title.replace('\t', ' ')
      title = title.replace('\r', ' ')
      title = title.replace('\n', ' ')
      while '  ' in title: 
         title = title.replace('  ', ' ')
      if len(title) > 200: 
         title = title[:200] + '[...]'
      
      def e(m): 
         entity = m.group(0)
         if entity.startswith('&#x'): 
            cp = int(entity[3:-1], 16)
            return unichr(cp).encode('utf-8')
         elif entity.startswith('&#'): 
            cp = int(entity[2:-1])
            return unichr(cp).encode('utf-8')
         else: 
            char = name2codepoint[entity[1:-1]]
            return unichr(char).encode('utf-8')
      title = r_entity.sub(e, title)

      if title: 
         try: title.decode('utf-8')
         except: 
            try: title = title.decode('iso-8859-1').encode('utf-8')
            except: title = title.decode('cp1252').encode('utf-8')
         else: pass
      else: title = '[The title is empty.]'

      title = title.replace('\n', '')
      title = title.replace('\r', '')
      self.msg(origin.sender, origin.nick + ': ' + title)
   else: self.msg(origin.sender, origin.nick + ': No title found')
f_title.commands = ['title', 'head']

def noteuri(code, input): 
   uri = input.group(1).encode('utf-8')
   if not hasattr(code.bot, 'last_seen_uri'): 
      code.bot.last_seen_uri = {}
   code.bot.last_seen_uri[input.sender] = uri
noteuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'
noteuri.priority = 'low'

if __name__ == '__main__': 
   print __doc__.strip()
