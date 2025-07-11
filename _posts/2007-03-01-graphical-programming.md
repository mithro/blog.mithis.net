---
author: mithro
categories:
- ideas
date: 2007-03-01T11:59:16+1000
excerpt: I spent today at a “conference” called NI Days, which was really just a day
  long pitch by National Instruments about their LabView software. It was however
  quite interesting, the two parts which caug....
layout: post
permalink: /archives/ideas/20-graphical-programming
title: Graphical Programming?
wordpress_category: ideas
wordpress_id: 20
wordpress_url: https://blog.mithis.net/archives/ideas/20-graphical-programming
---
I spent today at a “conference” called NI Days, which was really just a day long pitch by National Instruments about their LabView software. It was however quite interesting, the two parts which caught my attention where the “graphical programming” and the “dll importer”. 
The [graphical programming](http://en.wikipedia.org/wiki/Graphical_programming) worked by creating graphical boxes (which represent functions) and then wiring input and output together. The system looked like a very good for doing [parallel and concurrent systems](http://en.wikipedia.org/wiki/Concurrent_computing#Concurrent_programming_languages). 
The problem with our current programming languages, like [Python](http://python.org) is that it doesn’t scale well, both in performance and code development time, to multiple processor and concurrent systems. Things like [stackless](http://www.stackless.com/) and [greenlets](http://codespeak.net/py/dist/greenlet.html) are attempts to make this much easier. 
The problem with these “solutions” is that when using their system is then very hard to visualise where data is going and what critical paths exist (IE Where the system will block waiting for data). Graphical Programming would have a real advantage in this area. In the world of human resource scheduling, visualisation processes have long been used in the form of [Gantt charts (or Gnat chart as my brain keeps making me type)](http://en.wikipedia.org/wiki/Gantt_chart). 
Another problem with these systems is they are based around message passing. When you want to move around and process large blocks of continuous data (such as when you are doing [Software Defined Radio](http://www.gnu.org/software/gnuradio/) – which would otherwise fit perfectly into the blocked based concurrent systems) this sucks. The main reason the systems are based around message passing is because it gets rid of the problem of locks. Locking is the cause of most headaches in concurrent systems and involves horrible corner cases like “thread a has lock alpha and wants lock beta but thread b has lock beta and wants lock alpha”. By having data “flow” out of one system into another via a queue like structure (probably a circular queue for most systems) means many of these locking problems go away (as a queue is inherently lock safe). 
The other thing which caught my eye was the “dll importer” which look suspiciously like how the [ctypes code generator](http://docs.python.org/dev/lib/module-ctypes.html) works. The importer uses the C header file to figure out how to call C code in a DLL. It then “automagically” creates the graphical elements which you then places and wire like anything else in LabView.
I think you could easily build a basic graphical programming language very quickly using some type of existing canvas (maybe Dia, Inkscape or wxFloatCanvas). It’s then just a matter of doing a ctypes (which uses FFI and [gcc-xml](http://www.gccxml.org/HTML/Index.html)) like system to automatically generate the graphical elements for currently existing code. You would probably want to output run on something like the Erlang VM ([Erlang is a cool language with a syntax designed by retarded monkeys](http://www.erlang.org/)) so you have access to [microthreads](http://www.science.uva.nl/research/csa/microgrids.html). The result would be something which should be easy to use, scales well and already has a huge amount of code which can be used.
Actual implementation is left up to the reader as I just don’t have the time to do it :/. I need to concentrate on [Thousand Parsec](http://www.thousandparsec.net/), I may come back to it at some later date, but I doubt it. If you do end up doing something – please send me a line.
