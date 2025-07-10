---

author: mithro
categories:
- tp
date: 2009-01-27T16:22:22+1000
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/tp/95-xcompiling-cygwin-on-linux-for-windows
title: Compiling for Windows using Cygwin on Linux….
wayback_recovered: true
wordpress_category: tp
wordpress_id: 95
wordpress_url: https://blog.mithis.net/archives/tp/95-xcompiling-cygwin-on-linux-for-windows
comments:
  - id: 7628
    author: Ikem
    date: 2014-05-24T14:49:28+00:00
    content: |
      <p>The download link is broken.</p> <p>I found this alternative one: </p> <p><a href="http://www.thousandparsec.net/~tim/crosstool-cygwin-gcc336.tar.bz2" rel="nofollow">http://www.thousandparsec.net/~tim/crosstool-cygwin-gcc336.tar.bz2</a></p>
---
So for the past week while I have been at the [best conference](http://linux.conf.au/) in the world I have been trying to compile [tpserver-cpp](http://git.thousandparsec.net/gitweb/gitweb.cgi?p=tpserver-cpp.git;a=summary) for Windows. I had done the hard work and gotten it to compile (as documented [here](http://blog.mithis.net/archives/tp/10-compiling-tpserver-cpp-under-windows), [here](http://blog.mithis.net/archives/tp/12-compiling-tpserver-cpp-under-windows-part-2) and [here](http://blog.mithis.net/archives/tp/13-compiling-tpserver-cpp-under-windows-part-3)) on Windows previously. However, as I was in Hobart at a Linux conference I didn’t really have access to Windows computer. That was not going to stop me, so I attempted to [cross compile](http://en.wikipedia.org/wiki/Cross-compiling) the binaries under Linux. This has a number of advantages as it would mean when [someone](http://jms.id.au/wiki) finally gets around to creating a autobuilder, we can produce Windows binaries too.
Ubuntu provides the [mingw32 compilers](http://www.mingw.org/) in the [repository](http://packages.ubuntu.com/search?keywords=mingw32&searchon=names&section=all) so I didn’t think it would be all that hard to get working. The problem is that tpserver-cpp does not have a “native” Windows support but [cygwin](http://www.cygwin.com/) comes to the rescue and provides a compatibly layer. Using cygwin turned out to not be as simple as using mingw32 compiler with the cygwin headers.
I ended up using [crosstool](http://www.kegel.com/crosstool/) to build my own cygwin compiler. I battled for a long while with the fact that Ubuntu now enables “fortify source” by default. This breaks many versions of things like binutils and gcc (which often do *naughty* things which fortify source does not like). After I figured out how to disable it, I was still was only able to get an ancient version of gcc to compile (3.3.6) which meant I had to fix a lot of problems in the tpserver-cpp code. I guess someone had to do it eventually, but it was annoying that I was forced too.
I then manually downloaded a bunch of [cygwin packages](http://mirror.aarnet.edu.au/pub/cygwin/release/) to build a tree for the dependencies (such as boost and guile). This was much faster then trying to compile them on my own.  Finally, I was able to build tperver-cpp and create a Windows binary! I can confirm it runs fine under Wine and am now getting friends who are still shacked to Windows to test it there. 
It sounds much simpler now, but it took me over a week of work to boil it down to these steps. It was like a constant game of wack-a-mole, once I had solved one problem another popped up.
So what now in this area? I want to get a recent version of the compiler working and preferably build all the dependencies ourselves (rather then rely on the cygwin compiled versions). I would ultimately like to see the cygwin compilers being packaged with Ubuntu/Debian in the same way that the mingw32 compilers are. I don’t know if any of that is likely to happen however as I never seem to have enought time. For now I have uploaded a copy of [my cross compiler](http://blog.mithis.net/~tim/crosstool-cygwin-gcc336.tar.bz2) (It needs to be extracted so it is found in /opt/crosstool).
I hope this helps someone!
## Comments
**Ikem** -     <time datetime="2014-05-24T14:49:28+00:00">2014-05-24</time>
The download link is broken.
I found this alternative one: 
[http://www.thousandparsec.net/~tim/crosstool-cygwin-gcc336.tar.bz2](http://www.thousandparsec.net/~tim/crosstool-cygwin-gcc336.tar.bz2)
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
