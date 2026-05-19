---
author: mithro
categories:
- tp
- rcs-darcs
- tailor
date: 2007-04-21T08:17:42+1000
excerpt: 'As our code repositories for Thousand Parsec where down anyway (because
  of the host being compromised), we decided to do something we had been thinking
  about for a while.....'
layout: post
permalink: /archives/tp/35-using-tailor-to-go-to-git
title: Using Tailor to go to git
wordpress_category: tp
wordpress_id: 35
wordpress_url: https://blog.mithis.net/archives/tp/35-using-tailor-to-go-to-git
---
As our code repositories for Thousand Parsec where down anyway ([because of the host being compromised](http://www.thousandparsec.net/tp/news.php/2007-04-14-1400)), we decided to do something we had been thinking about for a while. We converted all our code repositories to git.

We had previously been using [darcs](http://darcs.net), however the unbounded memory usage was getting out of hand. The straw which broke the camel’s back was when nash couldn’t even checkout the web repository because darcs kept getting killed by the Out of Memory Manager (on a machine which has more then 512Mb of RAM).

After much discussion we decided to move to [git](http://git.or.cz/). The biggest reason we choose to use git was that we didn’t want to get stuck with another non-mainstream SCM system. With large people like [Xorg](http://www.freedesktop.org/wiki/Infrastructure/git), the [Linux Kernel](http://www.kernel.org/) and many others, I’m pretty sure git will become the SCM of choice in the near future.

As I had previously had a large amount of experience [converting the darcs repositories to subversion](http://blog.mithis.com/2007/02/25/using-tailor-creating-subversion-repository-for-thousand-parsec/) (for our mirrors), I was put in charge of converting the repositories to git. As previously, I used [Tailor](http://progetti.arstecnica.it/tailor).

The first problem is that darcs has [git repository support](http://darcs.net/DarcsWiki/DarcsGit). The suppose solution to this is using [disjunct working directories](http://progetti.arstecnica.it/tailor/wiki/DisjunctWorkingDirectories). However, git did not appear to like this, I need to hack up the source code to get it to work. I’ve submitted the patches back the Tailor repository and they have already been included!

Another problem I ran into was that I don’t have a machine which has enough memory to convert the web repository! I don’t have a computer with more then 768mb of ram (feel free to send me some more if you want! :P). Luckily thanks to the [Summer of Code](http://code.google.com/soc/), a student who goes by the name cherez (who I was very disappointed we didn’t have enough slots to select) gave me a shell account on his machine with 4Gb of Ram.

As a result of converting to git, I was also able to merge the development and stable branches (of both tpclient-pywx and libtpclient-py) into one repository. This was a little bit trickier then I would have liked, it involved finding the branch point manually and then telling tailor about it, in the end it worked out. You can find a copy of the config I used for branching [here](http://www.thousandparsec.net/~tim/tailor/tpclient-pywx-dev.tailor).

You can see the results of our conversion at our [gitweb](http://git.thousandparsec.net/).

I have to say, I’m amazed by git. Every single operation is very, very fast, I guess it’s why they called themselves “Git – Fast Version Control System”. Another thing that amazes me is the size of the repositories, under darcs our repositories where about 4Gb, with git they are around 200Mb! Overall, I’m happy with our choice.
