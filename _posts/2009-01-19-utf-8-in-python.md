---
author: mithro
categories:
- python
date: '2009-01-19T13:24:08+10:00'
excerpt: This is not a post about using UTF-8 properly in Python, but doing evil,
  evil things. Python dutifully respects the $LANG environment variable on the terminal.
  It turns out that...
layout: post
permalink: /archives/python/91-utf-8-in-python
title: $#%#! UTF-8 in Python
wordpress_category: python
wordpress_id: 91
wordpress_url: https://blog.mithis.net/archives/python/91-utf-8-in-python
---

<div ><p>This is <b>not</b> a post about using UTF-8 properly in Python, but doing <i>evil, evil</i> things.</p><p>Python dutifully respects the $LANG environment variable on the terminal. It turns out that a lot of the time this variable is totally wrong, it’s set to something like C even though the terminal is UTF-8 encoding. </p><p>The problem is that there is no easy way to change a file’s encoding after it’s open, well until this horrible hack! The following code will force the output encoding of stdout to UTF-8 even if started with LANG=C.</p><blockquote><div ><table><tr><td ><pre  ><span ># License: MIT</span><span >try</span>:
    <span >print</span> u<span >"<span >\u</span>263A"</span><span >except</span><span >Exception</span><span >,</span> e:
    <span >print</span> e

<span >import</span><span >sys</span><span >print</span><span >sys</span>.<span >stdout</span>.<span >encoding</span><span >from</span> ctypes <span >import</span> pythonapi<span >,</span> py_object<span >,</span> c_char_p
PyFile_SetEncoding <span >=</span> pythonapi.<span >PyFile_SetEncoding</span>
PyFile_SetEncoding.<span >argtypes</span><span >=</span><span >(</span>py_object<span >,</span> c_char_p<span >)</span><span >if</span><span >not</span> PyFile_SetEncoding<span >(</span><span >sys</span>.<span >stdout</span><span >,</span><span >"UTF-8"</span><span >)</span>:
    <span >raise</span><span >ValueError</span><span >try</span>:
    <span >print</span> u<span >"<span >\u</span>263A"</span><span >except</span><span >Exception</span><span >,</span> e:
    <span >print</span> e</pre></td></tr></table></div></blockquote></div>