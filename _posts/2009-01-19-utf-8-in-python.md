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
This is **not** a post about using UTF-8 properly in Python, but doing *evil, evil* things.
Python dutifully respects the $LANG environment variable on the terminal. It turns out that a lot of the time this variable is totally wrong, it’s set to something like C even though the terminal is UTF-8 encoding. 
The problem is that there is no easy way to change a file’s encoding after it’s open, well until this horrible hack! The following code will force the output encoding of stdout to UTF-8 even if started with LANG=C.
> ```python
# License: MITtry:
print u"\u263A"exceptException, e:
print e
importsysprintsys.stdout.encodingfrom ctypes import pythonapi, py_object, c_char_p
PyFile_SetEncoding = pythonapi.PyFile_SetEncoding
PyFile_SetEncoding.argtypes=(py_object, c_char_p)ifnot PyFile_SetEncoding(sys.stdout,"UTF-8"):
raiseValueErrortry:
print u"\u263A"exceptException, e:
print e
```