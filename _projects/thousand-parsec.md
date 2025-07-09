---
layout: project
title: "Thousand Parsec Project"
description: "Open source framework for turn-based strategy games"
category: software
tags:
  - gaming
  - open source
  - strategy games
  - framework
  - python
status: inactive
github: https://github.com/thousandparsec
website: http://www.thousandparsec.net
---

# Thousand Parsec Project

Thousand Parsec is an open source framework for turn-based strategy games. The project aims to create a flexible platform that allows developers to create complex strategy games without having to reinvent the wheel.

## Key Features

- **Modular Architecture**: Separate client and server components
- **Multiple Game Rules**: Support for different game rule sets
- **Cross-platform**: Works on Linux, Windows, and macOS
- **Network Play**: Built-in support for multiplayer games
- **Extensible**: Plugin system for adding new features

## Related Blog Posts

{% assign related_posts = site.posts | where: "categories", "Tp" %}
{% for post in related_posts limit: 10 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}

## Links

- [Project Website](http://www.thousandparsec.net)
- [GitHub Organization](https://github.com/thousandparsec)
- [Documentation](http://www.thousandparsec.net/wiki/Main_Page)