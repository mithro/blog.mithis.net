---
author: mithro
categories:
- Tp
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

<div >
<p>To try and get our activity rating up on <a href="http://www.sf.net/projects/thousandparsec">SourceForge</a> I’m in the progress of trying to mirror our darcs repositories in SourceForge’s SVN repositories.</p>
<p>This would also be useful for things like <a href="http://www.ohloh.net/projects/3679">oholh</a> as JLP pointed out. It might make it easier for people to track the development version under Windows/Mac as they wouldn’t need to get a working darcs version.</p>
<p>To do this I need to use a program called <a href="http://progetti.arstecnica.it/tailor">Tailor</a> which lets you convert between a wide range of different SCM systems. It took me a while to get a combination of tailor, darcs and svn which seems to work okay.</p>
<p>What I ended up with is the following <a href="http://blog.mithis.net/wp-content/uploads/2007/02/darcs2svn-start.sh" title="Darcs to Subversion Conversion script.">Darcs to Subversion Conversion script.</a></p>
<p>Each time you run it, it rebuilds the svn repository from scratch. This was useful during testing so that I could get my comment formatting correct (and fiddle with the other settings).</p>
<p>A ran into another problem however, to use Tailor and get nice author and actual commit date you need the <a href="http://progetti.arstecnica.it/tailor/browser/README#L806">special hook</a> installed. This hook is just an <a href="http://svnbook.red-bean.com/en/1.0/ch05s02.html#svn-ch-5-sect-2.1">empty pre-revprop-change</a>. However, SourceForge in all their wisdom don’t have support for this yet, there is a <a href="https://sourceforge.net/tracker/?func=detail&aid=1480553&group_id=1&atid=350001">pending change request</a> but it hasn’t been touched in about 3 months. Here is hoping they figure out something in the near future. There have been about 20 requests if you do a search for pre-revprop-change.</p>
</div>