---

author: mithro
categories:
- python
date: 2009-01-20T09:29:49+1100
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/python/94-reading-cookies-firefox
title: Reading cookies from most Firefox versions…
wayback_recovered: true
wordpress_category: python
wordpress_id: 94
wordpress_url: https://blog.mithis.net/archives/python/94-reading-cookies-firefox
comments:
  - id: 7241
    author: thegreatgrateful
    date: 2010-06-08T23:20:35+00:00
    content: |
      <p>thanks man!</p>
  - id: 7243
    author: Will
    date: 2010-08-22T19:09:19+00:00
    content: |
      <p>I have the same error as Chris</p> <p>NameError: global name &#8216;ret&#8217; is not defined</p> <p>I am currently using the copy of firefox_finder.py and firefox3_repack.py from your repo.</p>
  - id: 7244
    author: Will
    date: 2010-08-22T19:17:01+00:00
    content: |
      <p>sorry about the previous comment, I went the the site listed in the script:</p> <p><a href="http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846" rel="nofollow">http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846</a></p> <p>I see that it uses on line 68:</p> <p> ret = _winreg.QueryValueEx(key, name)<br /> except WindowsError:<br /> return None<br /> else:<br /> key.Close()<br /> if ret[1] == _winreg.REG_EXPAND_SZ:<br /> return expandvars(ret[0])<br /> else:<br /> return ret[0]</p> <p>which your code closely mirrors :</p> <p> result = _winreg.QueryValueEx(key, &#8216;AppData&#8217;)<br /> except WindowsError:<br /> return None<br /> else:<br /> key.Close()<br /> if ret[1] == _winreg.REG_EXPAND_SZ:<br /> result = win32api.ExpandEnvironmentStrings(ret[0])<br /> else:<br /> result = ret[0]</p> <p>It&#8217;s just that you put result = as opposed to ret = on that first line and then used ret further on.</p>
  - id: 7245
    author: mithro
    date: 2010-08-23T05:49:46+00:00
    content: |
      <p>I&#8217;ve updated the code once more, it might work now. As I said I can&#8217;t actually test this code as I don&#8217;t have a windows computer.</p>
---
Yesterday, I wrote about how to reading the [cookies from Firefox 3.0](http://blog.mithis.net/archives/python/90-firefox3-cookies-in-python) from Python. This code snippet extends the previous example by adding code which finds the cookie file on various different operating systems (Windows, Linux and Mac OS X). Hope this helps people who need to do this.
> 
```python
#! /usr/bin/env python
# Reading the cookie's from Firefox/Mozilla. Supports Firefox 3.0 and Firefox 2.x
#
# Author: Noah Fontes , 
#         Tim Ansell 
# License: MIT
def sqlite2cookie(filename):
from cStringIO import StringIO
from pysqlite2 import dbapi2 as sqlite
con = sqlite.connect(filename)
cur = con.cursor()
cur.execute("select host, path, isSecure, expiry, name, value from moz_cookies")
ftstr = ["FALSE","TRUE"]
s = StringIO()
s.write("""\
# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.
""")
for item in cur.fetchall():
s.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
item[0], ftstr[item[0].startswith('.')], item[1],
ftstr[item[2]], item[3], item[4], item[5]))
s.seek(0)
cookie_jar = cookielib.MozillaCookieJar()
cookie_jar._really_load(s, '', True, True)
return cookie_jar
import cookielib
import os
import sys
import logging
import ConfigParser
# Set up cookie jar paths
def _get_firefox_cookie_jar (path):
profiles_ini = os.path.join(path, 'profiles.ini')
if not os.path.exists(path) or not os.path.exists(profiles_ini):
return None
# Open profiles.ini and read the path for the first profile
profiles_ini_reader = ConfigParser.ConfigParser();
profiles_ini_reader.readfp(open(profiles_ini))
profile_name = profiles_ini_reader.get('Profile0', 'Path', True)
profile_path = os.path.join(path, profile_name)
if not os.path.exists(profile_path):
return None
else:
if os.path.join(profile_path, 'cookies.sqlite'):
return os.path.join(profile_path, 'cookies.sqlite')
elif os.path.join(profile_path, 'cookies.txt'):
return os.path.join(profile_path, 'cookies.txt')
def _get_firefox_nt_cookie_jar ():
# See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846
try:
import _winreg
import win32api
except ImportError:
logging.error('Cannot load winreg -- running windows and win32api loaded?')
key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
try:
result = _winreg.QueryValueEx(key, 'AppData')
except WindowsError:
return None
else:
key.Close()
if ret[1] == _winreg.REG_EXPAND_SZ:
result = win32api.ExpandEnvironmentStrings(ret[0])
else:
result = ret[0]
return _get_firefox_cookie_jar(os.path.join(result, r'Mozilla\Firefox\Profiles'))
def _get_firefox_posix_cookie_jar ():
return _get_firefox_cookie_jar(os.path.expanduser(r'~/.mozilla/firefox'))
def _get_firefox_mac_cookie_jar ():
# First of all...
result = _get_firefox_cookie_jar(os.path.expanduser(r'~/Library/Mozilla/Firefox/Profiles'))
if result == None:
result = _get_firefox_cookie_jar(os.path.expanduser(r'~/Library/Application Support/Firefox/Profiles'))
return result
FIREFOX_COOKIE_JARS = {
'nt': _get_firefox_nt_cookie_jar,
'posix': _get_firefox_posix_cookie_jar,
'mac': _get_firefox_mac_cookie_jar
}
cookie_jar = None
try:
cookie_jar = FIREFOX_COOKIE_JARS[os.name]()
except KeyError:
cookie_jar = None
path = raw_input('Path to cookie jar file [%s]: ' % cookie_jar)
if path.strip():
# Some input specified, set it
cookie_jar = os.path.realpath(os.path.expanduser(path.strip()))
if cookie_jar.endswith('.sqlite'):
cookie_jar = sqlite2cookie(cookie_jar)
else:
cookie_jar = cookielib.MozillaCookieJar(cookie_jar)
```
*Edit: The latest version of this code can be found at [http://blog.mithis.com/cgi-bin/gitweb.cgi](http://blog.mithis.com/cgi-bin/gitweb.cgi) and includes numerous fixes and updates.*
## Comments
**thegreatgrateful** -     <time datetime="2010-06-08T23:20:35+00:00">2010-06-08</time>
thanks man!
**Will** -     <time datetime="2010-08-22T19:09:19+00:00">2010-08-22</time>
I have the same error as Chris
NameError: global name 'ret' is not defined
I am currently using the copy of firefox_finder.py and firefox3_repack.py from your repo.
**Will** -     <time datetime="2010-08-22T19:17:01+00:00">2010-08-22</time>
sorry about the previous comment, I went the the site listed in the script:
[http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846](http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846)
I see that it uses on line 68:
ret = _winreg.QueryValueEx(key, name)
except WindowsError:
return None
else:
key.Close()
if ret[1] == _winreg.REG_EXPAND_SZ:
return expandvars(ret[0])
else:
return ret[0]
which your code closely mirrors :
result = _winreg.QueryValueEx(key, 'AppData')
except WindowsError:
return None
else:
key.Close()
if ret[1] == _winreg.REG_EXPAND_SZ:
result = win32api.ExpandEnvironmentStrings(ret[0])
else:
result = ret[0]
It's just that you put result = as opposed to ret = on that first line and then used ret further on.
**mithro** -     <time datetime="2010-08-23T05:49:46+00:00">2010-08-23</time>
I've updated the code once more, it might work now. As I said I can't actually test this code as I don't have a windows computer.
<style>
.comments {
margin-top: 2rem;
border-top: 1px solid #eee;
padding-top: 2rem;
}
.comment {
margin-bottom: 1.5rem;
padding: 1rem;
background: #f9f9f9;
border-left: 4px solid #ddd;
}
.comment-meta {
font-size: 0.9rem;
color: #666;
margin-bottom: 0.5rem;
}
.comment-content {
line-height: 1.6;
}
.comment-content p {
margin: 0.5rem 0;
}
</style>
