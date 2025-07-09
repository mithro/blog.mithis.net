---
author: mithro
categories:
- Python
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

<div >
<p>I found the following code snippet on my hard drive today. It allows you to access <a href="http://www.getfirefox.com/" target="_self">Firefox 3.x</a> cookies in Python. Firefox 3.x moved away from the older text file format to a <a href="http://www.sqlite.org/">sqlite</a> database.</p>
<p>This code is useful if you want to access something behind an authentication gateway and you also access the page through your web browser. You can also use this code to convert a sqlite database into a cookie file <a href="http://curl.haxx.se/">CURL</a> can read.</p>
<p>I didn’t write this code, it was written by Noah Fontes when we where doing some scraping of the <a href="http://code.google.com/soc">Google Summer of Code</a> website (before I joined Google).</p>
<blockquote>
<div ><table><tr><td ><pre  ><span >#! /usr/bin/env python</span>
<span ># Protocol implementation for handling gsocmentors.com transactions</span>
<span ># Author: Noah Fontes nfontes AT cynigram DOT com</span>
<span ># License: MIT</span>
 
<span >def</span> sqlite2cookie<span >(</span>filename<span >)</span>:
    <span >from</span> <span >cStringIO</span> <span >import</span> <span >StringIO</span>
    <span >from</span> pysqlite2 <span >import</span> dbapi2 <span >as</span> sqlite
 
    con <span >=</span> sqlite.<span >connect</span><span >(</span>filename<span >)</span>
 
    cur <span >=</span> con.<span >cursor</span><span >(</span><span >)</span>
    cur.<span >execute</span><span >(</span><span >"select host, path, isSecure, expiry, name, value from moz_cookies"</span><span >)</span>
 
    ftstr <span >=</span> <span >[</span><span >"FALSE"</span><span >,</span><span >"TRUE"</span><span >]</span>
 
    s <span >=</span> <span >StringIO</span><span >(</span><span >)</span>
    s.<span >write</span><span >(</span><span >"""<span >\</span>
# Netscape HTTP Cookie File
# http://www.netscape.com/newsref/std/cookie_spec.html
# This is a generated file!  Do not edit.
"""</span><span >)</span>
    <span >for</span> item <span >in</span> cur.<span >fetchall</span><span >(</span><span >)</span>:
        s.<span >write</span><span >(</span><span >"%s<span >\t</span>%s<span >\t</span>%s<span >\t</span>%s<span >\t</span>%s<span >\t</span>%s<span >\t</span>%s<span >\n</span>"</span> % <span >(</span>
            item<span >[</span><span >0</span><span >]</span><span >,</span> ftstr<span >[</span>item<span >[</span><span >0</span><span >]</span>.<span >startswith</span><span >(</span><span >'.'</span><span >)</span><span >]</span><span >,</span> item<span >[</span><span >1</span><span >]</span><span >,</span>
            ftstr<span >[</span>item<span >[</span><span >2</span><span >]</span><span >]</span><span >,</span> item<span >[</span><span >3</span><span >]</span><span >,</span> item<span >[</span><span >4</span><span >]</span><span >,</span> item<span >[</span><span >5</span><span >]</span><span >)</span><span >)</span>
 
    s.<span >seek</span><span >(</span><span >0</span><span >)</span>
 
    cookie_jar <span >=</span> <span >cookielib</span>.<span >MozillaCookieJar</span><span >(</span><span >)</span>
    cookie_jar._really_load<span >(</span>s<span >,</span> <span >''</span><span >,</span> <span >True</span><span >,</span> <span >True</span><span >)</span>
    <span >return</span> cookie_jar</pre></td></tr></table></div>
</blockquote>
</div>