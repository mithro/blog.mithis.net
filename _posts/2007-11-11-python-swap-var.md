---

author: mithro
categories:
- ideas
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

<div >
<p>Some people say “you learn something new everyday” or something like that. Today someone on <a href="http://web.archive.org/web/20081121144250/irc://irc.freenode.org/#python">#python</a> showed me a cool trick I never would have thought of on my own.</p>
<p>Often there is a time when you want to swap the contents of two variables. The most popular way to do this is using a third variable as shown below:</p>
<blockquote><p>
temp = a<br/>
a = b<br/>
b = temp
</p></blockquote>
<p>This looks sucky and doesn’t really express very well what you want to do. A much better way to do this in Python is with the following magic line:</p>
<blockquote><p>
a, b = b, a
</p></blockquote>
<p>Doesn’t that look so much better? And it is very clear to anyone who has used Python before what is going on. To think, I have been using Python for about 7 years now and never thought of doing that.</p>
<p>Just thought I would share this tidbit.</p>
</div>

## Comments

<div class="comments">
<div class="comment" id="comment-7246">
  <div class="comment-meta">
    <strong>Anel</strong> -     <time datetime="2010-10-11T17:26:30+00:00">2010-10-11</time>
  </div>
  <div class="comment-content">
    <p>Haha, nice joke, guys&#8230;))</p>
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
