---

author: mithro
categories:
- ideas
- python
date: 2007-11-11T00:37:39-0500
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/ideas/64-python-swap-var
title: Cool Python, Swaping two variables
wayback_recovered: true
wordpress_category: ideas
wordpress_id: 64
wordpress_url: https://blog.mithis.net/archives/ideas/64-python-swap-var
comments:
  - id: 7246
    author: Anel
    date: 2010-10-11T17:26:30+00:00
    content: |
      <p>Haha, nice joke, guys&#8230;))</p>
---
Some people say “you learn something new everyday” or something like that. Today someone on [#python](http://web.archive.org/web/20081121144250/irc://irc.freenode.org/#python) showed me a cool trick I never would have thought of on my own.
Often there is a time when you want to swap the contents of two variables. The most popular way to do this is using a third variable as shown below:
> 
temp = a
a = b
b = temp
This looks sucky and doesn’t really express very well what you want to do. A much better way to do this in Python is with the following magic line:
> 
a, b = b, a
Doesn’t that look so much better? And it is very clear to anyone who has used Python before what is going on. To think, I have been using Python for about 7 years now and never thought of doing that.
Just thought I would share this tidbit.
## Comments
**Anel** -     <time datetime="2010-10-11T17:26:30+00:00">2010-10-11</time>
Haha, nice joke, guys&#8230;))
