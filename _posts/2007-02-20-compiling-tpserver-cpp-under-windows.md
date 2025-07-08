---
author: mithro
categories:
- Tp
date: 2007-02-20T07:39:04+1000
excerpt: I had hoped that compiling tpserver-cpp under windows would be easy. Turns
  out I was very, very wrong. I am even going the easy route of using Cygwin to handle
  all the select/signal/pthread stuff whi....
layout: post
permalink: /archives/tp/10-compiling-tpserver-cpp-under-windows
title: Compiling tpserver-cpp under windows.
wordpress_category: tp
wordpress_id: 10
wordpress_url: https://blog.mithis.net/archives/tp/10-compiling-tpserver-cpp-under-windows
---

<div >
<p>I had hoped that compiling tpserver-cpp under windows would be easy. Turns out I was very, very wrong. I am even going the easy route of using <a href="http://cygwin.com/">Cygwin</a> to handle all the select/signal/pthread stuff which wouldn’t work easily under Microsoft products.</p>
<p>Compiling it was relatively easy once I had all the dependencies installed. Cygwin comes out of the box with <a href="http://www.gnu.org/software/guile/guile.html">guile (1.6 and 1.8)</a> which was the only dependency I was concerned about. (Everything else is pretty standard.)</p>
<p>However, this is where I ran into a problem. The server uses shared libraries to contain important modules like game rule data and persistence. This doesn’t work to well under Windows. At first I should it should just be an easy step of convincing the autotools to build .dll versions of the modules. Turns out dll’s aren’t at all like .so files. They have to have “no unresolved symbols” which makes it very hard to do what tpserver-cpp does (IE modules use the core functions in the main server like the logger).</p>
<p>Next step was to find out what other applications did, I found this library made by <a href="http://www.gnu.org/software/libtool/manual.html#Using-libltdl">libtool guys called ‘libltdl’</a> which lets you “fake” dlopen stuff. So I “ported” tpserver-cpp to use this instead of just a raw dlopen. (This should also make tpserver-cpp more portable to such weird operating systems as BeOS and HPUX.) Dunno if Lee will like it or not 🙂</p>
<p>Still not done yet but it’s looking much more hopeful.</p>
</div>