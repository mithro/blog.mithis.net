---
author: mithro
categories:
- tp
date: 2007-02-25T15:01:22+1000
excerpt: 'To try and get our activity rating up on SourceForge I’m in the progress
  of trying to mirror our darcs repositories in SourceForge’s SVN repositories.

  This would also be useful for things like oholh.....'
layout: post
permalink: /archives/tp/16-tailor-darcs2svn-tp
title: Using Tailor – Creating Subversion Repository for Thousand Parsec
wordpress_category: tp
wordpress_id: 16
wordpress_url: https://blog.mithis.net/archives/tp/16-tailor-darcs2svn-tp
---
To try and get our activity rating up on [SourceForge](http://www.sf.net/projects/thousandparsec) I’m in the progress of trying to mirror our darcs repositories in SourceForge’s SVN repositories.
This would also be useful for things like [oholh](http://www.ohloh.net/projects/3679) as JLP pointed out. It might make it easier for people to track the development version under Windows/Mac as they wouldn’t need to get a working darcs version.
To do this I need to use a program called [Tailor](http://progetti.arstecnica.it/tailor) which lets you convert between a wide range of different SCM systems. It took me a while to get a combination of tailor, darcs and svn which seems to work okay.
What I ended up with is the following [Darcs to Subversion Conversion script.](http://blog.mithis.net/wp-content/uploads/2007/02/darcs2svn-start.sh)
Each time you run it, it rebuilds the svn repository from scratch. This was useful during testing so that I could get my comment formatting correct (and fiddle with the other settings).
A ran into another problem however, to use Tailor and get nice author and actual commit date you need the [special hook](http://progetti.arstecnica.it/tailor/browser/README#L806) installed. This hook is just an [empty pre-revprop-change](http://svnbook.red-bean.com/en/1.0/ch05s02.html#svn-ch-5-sect-2.1). However, SourceForge in all their wisdom don’t have support for this yet, there is a [pending change request](https://sourceforge.net/tracker/?func=detail&aid=1480553&group_id=1&atid=350001) but it hasn’t been touched in about 3 months. Here is hoping they figure out something in the near future. There have been about 20 requests if you do a search for pre-revprop-change.
