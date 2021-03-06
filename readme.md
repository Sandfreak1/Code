Code the flexible Python IRC Bot
================================

Build State: [![Build Status](http://build.liamstanley.net/job/Code/badge/icon)](http://build.liamstanley.net/job/Code/)

Code (on #L @ irc.esper.net) is a open source python IRC bot forked from Phenny/Jenni, with new modules, easier to understand commands, and easy installation! Code can run on any operating system that supports Python 2.4 or higher.

Features
-------- 
________

Code is packed full of features ranging from raw IRC functions to modules that can be unloaded and loaded with ease. Some features include:

Fast & Light Weight
- Code is very small, so it won't take up resources. Also, Code is very responsive and quick-paced! Also he can run in 1-2 processes!

Load & Unload Modules
- Code has the ability to load user defined IRC modules, that are pre-made or ones that you create. Code also can live-reload modules for active and fast development.

Very User Friendly
- It is very easy to install and run Code, even if you have no knowledge of ever running a IRC bot before. ".help" commands, and friendly responses help everything feel smooth and elegant.

Easy-To-use API
- When creating your own modules, it is always very easy to have a fully documented API and easy to understand functions.

Open-Source
- Found a bug, feature, or technical support/advice? You can always navigate to the [Github](https://github.com/Liamraystanley/Code) page to make requests and post bugs. Heck, even fork Code as your own and make your own modifications!</dd>

Configuration
- By default, Code has the ability to change his username (including NickServ Authentication), server (including server password), and excluded channel/modules.

Installation - How do I install? 
================================
________________________________

 > for rss.py to work, install feedparser via your pip/yum/other package installer.

**If you have any isues during the install, feel free to head to http://chat.liamstanley.net/ to get help**

1) Run `git clone https://github.com/Liamraystanley/Code.git` - if you do not have git installed, 
simply install it via your package manager. e.i, `sudo apt-get install git`
2) Run `./code`- this creates a default config file 
3) Edit ~/.code/default.py 
4) Run `./code` - this now runs code with your settings 

Full command would be: 

    python ./code
    home/code/lib/python272 ./code
    
(full path purposes) 

If you wish to run Code on a UNIX shell, the best thing to do would be to fork it to the background process usign nohup, you do this by execution python/Code with: 

    nohup python ./code &

The `nohup` and `&` play a crucial part in forking itself to the background. If this method 'still' doesn't work, you need to try these commands. (you need to use the method above, THEN cancel out of the current process (I use CTRL+C on windows keyboards)) 

    bg
    disown -h

Another method of forking it into the background, is by using the well-known linux program called screen.

    screen python ./code

This creates a terminal window that can be logged into and out without disturbing the process in that window. to exit the screen safely, hit `CTRL+A` then `CTRL+D`.
To log back into, and view the playback of Code, type `screen -r`.


Configuration & Personalization 
===============================
_______________________________

Warning! Once you install Code using the method above, you need to configure him to point to the server you wish to connect him to, as well as add a module path, and administrators/owners.

Unix & Unix-like OS: 
--------------------

Edit the file located at `../.code/default.py`. this is either the previous directory, or your $HOME directory `/home/(user)`.

Windows
-------

Edit the file located in your Documents folder, which should be located at: 
`C:\\users\myusername\.code\default.py`
`default.py` might be located in the same spot as the UNIX location listed above.
You should see a file like this:

```python
# Code Copyright (C) 2012-2013 Liam Stanley
# Uncomment things you wish to add to the file
# lines with "#" in front of them are comments

# irc bot nickname
nick = 'code'
# irc server host
host = 'irc.example.net'
# port to use to connect
port = '6667'
#channels to auto-join
channels = ['#example', '#test']
#your nickname for use in admin functions
owner = 'yournickname'
# website to show for help documentation
website = 'http://code.liamstanley.net'

# password is the Nickserv password, serverpass is the server password
# password = 'example'
# serverpass = 'serverpass'

# These are people who will be able to use admin.py's functions...
admins = [owner, 'someoneyoutrust']
# But admin.py is disabled by default, as follows:
exclude = ['admin', 'mcbot', 'rss', 'twss']

# If you want to enumerate a list of modules rather than disabling
# some, use "enable = ['example']", which takes precedent over exclude
# 
# enable = []

# Directories to load user modules from
# e.g. /path/to/my/modules
extra = []

# Services to load: maps channel names to white or black lists
external = { 
  '#ponycode': ['!'], # allow all
  '#L': [], # allow none
  '*': ['!'] # default whitelist, allow all
}

# EOF
```

you should uncomment, and replace the necessary items (like serverpass & nickservpass) to run your bot. 

Customize Even More: 
====================
____________________

Changing Prefix: 
(this would be in the config, i jsut haven't gotten aroudn to it yet. sorry!)

If you wish to change the command prefix from "." to another item Edit /code/code and find this: 

```python
    if not hasattr(module, 'prefix'):
        module.prefix = r'\.'
```

And change it to: 

```python
    if not hasattr(module, 'prefix'):
        module.prefix = r'\(CustomPrefix)'
```

Licensing
---------
_________

Code Copyright (C) 2012-2013 Liam Stanley (More info here: http://code.liamstanley.net/#license)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

The original license from Jenni and Phenny

       Eiffel Forum License, version 2
    
    1. Permission is hereby granted to use, copy, modify and/or
       distribute this package, provided that:
          * copyright notices are retained unchanged,
          * any distribution of this package, whether modified or not,
            includes this license text.
    2. Permission is hereby also granted to distribute binary programs
       which depend on this package. If the binary program depends on a
       modified version of this package, you are encouraged to publicly
       release the modified version of this package.
    
    THIS PACKAGE IS PROVIDED "AS IS" AND WITHOUT WARRANTY. ANY EXPRESS OR
    IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE AUTHORS BE LIABLE TO ANY PARTY FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES ARISING IN ANY WAY OUT OF THE USE OF THIS PACKAGE.
