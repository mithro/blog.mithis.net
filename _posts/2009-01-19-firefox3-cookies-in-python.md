---
author: mithro
categories:
- python
date: 2009-01-19T12:58:28+1000
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/python/90-firefox3-cookies-in-python
title: Reading Firefox 3.x cookies in Python
wayback_recovered: true
wordpress_category: python
wordpress_id: 90
wordpress_url: https://blog.mithis.net/archives/python/90-firefox3-cookies-in-python
---
I found the following code snippet on my hard drive today. It allows you to access [Firefox 3.x](http://www.getfirefox.com/) cookies in Python. Firefox 3.x moved away from the older text file format to a [sqlite](http://www.sqlite.org/) database.
This code is useful if you want to access something behind an authentication gateway and you also access the page through your web browser. You can also use this code to convert a sqlite database into a cookie file [CURL](http://curl.haxx.se/) can read.
I didn’t write this code, it was written by Noah Fontes when we where doing some scraping of the [Google Summer of Code](http://code.google.com/soc) website (before I joined Google).
> 
```python
#! /usr/bin/env python
# Protocol implementation for handling gsocmentors.com transactions
# Author: Noah Fontes nfontes AT cynigram DOT com
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
```
