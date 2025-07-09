---

author: mithro
categories:
- Python
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

<div >
<p>Yesterday, I wrote about how to reading the <a href="http://blog.mithis.net/archives/python/90-firefox3-cookies-in-python">cookies from Firefox 3.0</a> from Python. This code snippet extends the previous example by adding code which finds the cookie file on various different operating systems (Windows, Linux and Mac OS X). Hope this helps people who need to do this.</p>
<blockquote>
<div ><table><tr><td ><pre  ><span >#! /usr/bin/env python</span>
<span ># Reading the cookie's from Firefox/Mozilla. Supports Firefox 3.0 and Firefox 2.x</span>
<span >#</span>
<span ># Author: Noah Fontes <nfontes AT cynigram DOT com>, </span>
<span >#         Tim Ansell <mithro AT mithis DOT com></span>
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
    <span >return</span> cookie_jar
 
<span >import</span> <span >cookielib</span>
<span >import</span> <span >os</span>
<span >import</span> <span >sys</span>
<span >import</span> <span >logging</span>
<span >import</span> <span >ConfigParser</span>
 
<span ># Set up cookie jar paths</span>
<span >def</span> _get_firefox_cookie_jar <span >(</span>path<span >)</span>:
    profiles_ini <span >=</span> <span >os</span>.<span >path</span>.<span >join</span><span >(</span>path<span >,</span> <span >'profiles.ini'</span><span >)</span>
    <span >if</span> <span >not</span> <span >os</span>.<span >path</span>.<span >exists</span><span >(</span>path<span >)</span> <span >or</span> <span >not</span> <span >os</span>.<span >path</span>.<span >exists</span><span >(</span>profiles_ini<span >)</span>:
        <span >return</span> <span >None</span>
 
    <span ># Open profiles.ini and read the path for the first profile</span>
    profiles_ini_reader <span >=</span> <span >ConfigParser</span>.<span >ConfigParser</span><span >(</span><span >)</span><span >;</span>
    profiles_ini_reader.<span >readfp</span><span >(</span><span >open</span><span >(</span>profiles_ini<span >)</span><span >)</span>
    profile_name <span >=</span> profiles_ini_reader.<span >get</span><span >(</span><span >'Profile0'</span><span >,</span> <span >'Path'</span><span >,</span> <span >True</span><span >)</span>
 
    profile_path <span >=</span> <span >os</span>.<span >path</span>.<span >join</span><span >(</span>path<span >,</span> profile_name<span >)</span>
    <span >if</span> <span >not</span> <span >os</span>.<span >path</span>.<span >exists</span><span >(</span>profile_path<span >)</span>:
        <span >return</span> <span >None</span>
    <span >else</span>:
        <span >if</span> <span >os</span>.<span >path</span>.<span >join</span><span >(</span>profile_path<span >,</span> <span >'cookies.sqlite'</span><span >)</span>:
            <span >return</span> <span >os</span>.<span >path</span>.<span >join</span><span >(</span>profile_path<span >,</span> <span >'cookies.sqlite'</span><span >)</span>
        <span >elif</span> <span >os</span>.<span >path</span>.<span >join</span><span >(</span>profile_path<span >,</span> <span >'cookies.txt'</span><span >)</span>:
            <span >return</span> <span >os</span>.<span >path</span>.<span >join</span><span >(</span>profile_path<span >,</span> <span >'cookies.txt'</span><span >)</span>
 
<span >def</span> _get_firefox_nt_cookie_jar <span >(</span><span >)</span>:
    <span ># See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846</span>
    <span >try</span>:
        <span >import</span> <span >_winreg</span>
        <span >import</span> win32api
    <span >except</span> <span >ImportError</span>:
        <span >logging</span>.<span >error</span><span >(</span><span >'Cannot load winreg -- running windows and win32api loaded?'</span><span >)</span>
    key <span >=</span> <span >_winreg</span>.<span >OpenKey</span><span >(</span><span >_winreg</span>.<span >HKEY_CURRENT_USER</span><span >,</span> r<span >'Software<span >\M</span>icrosoft<span >\W</span>indows<span >\C</span>urrentVersion<span >\E</span>xplorer<span >\S</span>hell Folders'</span><span >)</span>
    <span >try</span>:
        result <span >=</span> <span >_winreg</span>.<span >QueryValueEx</span><span >(</span>key<span >,</span> <span >'AppData'</span><span >)</span>
    <span >except</span> <span >WindowsError</span>:
        <span >return</span> <span >None</span>
    <span >else</span>:
        key.<span >Close</span><span >(</span><span >)</span>
        <span >if</span> ret<span >[</span><span >1</span><span >]</span> <span >==</span> <span >_winreg</span>.<span >REG_EXPAND_SZ</span>:
            result <span >=</span> win32api.<span >ExpandEnvironmentStrings</span><span >(</span>ret<span >[</span><span >0</span><span >]</span><span >)</span>
        <span >else</span>:
            result <span >=</span> ret<span >[</span><span >0</span><span >]</span>
 
    <span >return</span> _get_firefox_cookie_jar<span >(</span><span >os</span>.<span >path</span>.<span >join</span><span >(</span>result<span >,</span> r<span >'Mozilla<span >\F</span>irefox<span >\P</span>rofiles'</span><span >)</span><span >)</span>
 
<span >def</span> _get_firefox_posix_cookie_jar <span >(</span><span >)</span>:
    <span >return</span> _get_firefox_cookie_jar<span >(</span><span >os</span>.<span >path</span>.<span >expanduser</span><span >(</span>r<span >'~/.mozilla/firefox'</span><span >)</span><span >)</span>
 
<span >def</span> _get_firefox_mac_cookie_jar <span >(</span><span >)</span>:
    <span ># First of all...</span>
    result <span >=</span> _get_firefox_cookie_jar<span >(</span><span >os</span>.<span >path</span>.<span >expanduser</span><span >(</span>r<span >'~/Library/Mozilla/Firefox/Profiles'</span><span >)</span><span >)</span>
    <span >if</span> result <span >==</span> <span >None</span>:
        result <span >=</span> _get_firefox_cookie_jar<span >(</span><span >os</span>.<span >path</span>.<span >expanduser</span><span >(</span>r<span >'~/Library/Application Support/Firefox/Profiles'</span><span >)</span><span >)</span>
    <span >return</span> result
 
FIREFOX_COOKIE_JARS <span >=</span> <span >{</span>
    <span >'nt'</span>: _get_firefox_nt_cookie_jar<span >,</span>
    <span >'posix'</span>: _get_firefox_posix_cookie_jar<span >,</span>
    <span >'mac'</span>: _get_firefox_mac_cookie_jar
<span >}</span>
 
cookie_jar <span >=</span> <span >None</span>
<span >try</span>:
    cookie_jar <span >=</span> FIREFOX_COOKIE_JARS<span >[</span><span >os</span>.<span >name</span><span >]</span><span >(</span><span >)</span>
<span >except</span> <span >KeyError</span>:
    cookie_jar <span >=</span> <span >None</span>
 
path <span >=</span> <span >raw_input</span><span >(</span><span >'Path to cookie jar file [%s]: '</span> % cookie_jar<span >)</span>
<span >if</span> path.<span >strip</span><span >(</span><span >)</span>:
    <span ># Some input specified, set it</span>
    cookie_jar <span >=</span> <span >os</span>.<span >path</span>.<span >realpath</span><span >(</span><span >os</span>.<span >path</span>.<span >expanduser</span><span >(</span>path.<span >strip</span><span >(</span><span >)</span><span >)</span><span >)</span>
 
<span >if</span> cookie_jar.<span >endswith</span><span >(</span><span >'.sqlite'</span><span >)</span>:
    cookie_jar <span >=</span> sqlite2cookie<span >(</span>cookie_jar<span >)</span>
<span >else</span>:
    cookie_jar <span >=</span> <span >cookielib</span>.<span >MozillaCookieJar</span><span >(</span>cookie_jar<span >)</span></pre></td></tr></table></div>
</blockquote>
<p><i>Edit: The latest version of this code can be found at <a href="http://blog.mithis.com/cgi-bin/gitweb.cgi">http://blog.mithis.com/cgi-bin/gitweb.cgi</a> and includes numerous fixes and updates.</i></p>
</div>

## Comments

<div class="comments">
<div class="comment" id="comment-7241">
  <div class="comment-meta">
    <strong>thegreatgrateful</strong> -     <time datetime="2010-06-08T23:20:35+00:00">2010-06-08</time>
  </div>
  <div class="comment-content">
    <p>thanks man!</p>
  </div>
</div>

<div class="comment" id="comment-7243">
  <div class="comment-meta">
    <strong>Will</strong> -     <time datetime="2010-08-22T19:09:19+00:00">2010-08-22</time>
  </div>
  <div class="comment-content">
    <p>I have the same error as Chris</p> <p>NameError: global name &#8216;ret&#8217; is not defined</p> <p>I am currently using the copy of firefox_finder.py and firefox3_repack.py from your repo.</p>
  </div>
</div>

<div class="comment" id="comment-7244">
  <div class="comment-meta">
    <strong>Will</strong> -     <time datetime="2010-08-22T19:17:01+00:00">2010-08-22</time>
  </div>
  <div class="comment-content">
    <p>sorry about the previous comment, I went the the site listed in the script:</p> <p><a href="http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846" rel="nofollow">http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/473846</a></p> <p>I see that it uses on line 68:</p> <p> ret = _winreg.QueryValueEx(key, name)<br /> except WindowsError:<br /> return None<br /> else:<br /> key.Close()<br /> if ret[1] == _winreg.REG_EXPAND_SZ:<br /> return expandvars(ret[0])<br /> else:<br /> return ret[0]</p> <p>which your code closely mirrors :</p> <p> result = _winreg.QueryValueEx(key, &#8216;AppData&#8217;)<br /> except WindowsError:<br /> return None<br /> else:<br /> key.Close()<br /> if ret[1] == _winreg.REG_EXPAND_SZ:<br /> result = win32api.ExpandEnvironmentStrings(ret[0])<br /> else:<br /> result = ret[0]</p> <p>It&#8217;s just that you put result = as opposed to ret = on that first line and then used ret further on.</p>
  </div>
</div>

<div class="comment" id="comment-7245">
  <div class="comment-meta">
    <strong>mithro</strong> -     <time datetime="2010-08-23T05:49:46+00:00">2010-08-23</time>
  </div>
  <div class="comment-content">
    <p>I&#8217;ve updated the code once more, it might work now. As I said I can&#8217;t actually test this code as I don&#8217;t have a windows computer.</p>
  </div>
</div>

</div>

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
