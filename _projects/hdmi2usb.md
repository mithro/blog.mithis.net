---
layout: project
title: "HDMI2USB Project"
description: "Open source HDMI capture device for recording and streaming conferences"
category: hardware
tags:
  - HDMI
  - USB
  - FPGA
  - hardware
  - open source
status: active
github: https://github.com/timvideos/HDMI2USB
website: https://hdmi2usb.tv
---

# HDMI2USB Project

The HDMI2USB project develops affordable hardware options to record and stream HD videos (from HDMI & DisplayPort sources) for conferences, meetings and user groups.

## Key Features

- **Open Source Hardware**: All designs are released under open source licenses
- **FPGA-based**: Uses Xilinx Spartan-6 FPGA for video processing
- **USB 2.0 Interface**: Standard USB connection for easy integration
- **Real-time Processing**: Low latency video capture and streaming
- **Multiple Input Support**: HDMI and DisplayPort inputs

## Related Blog Posts

{% assign related_posts = site.posts | where: "categories", "Timvideos Us" %}
{% for post in related_posts limit: 10 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}

## Links

- [Project Website](https://hdmi2usb.tv)
- [GitHub Repository](https://github.com/timvideos/HDMI2USB)
- [Documentation](https://hdmi2usb.readthedocs.io)
- [Hardware Designs](https://github.com/timvideos/HDMI2USB-hardware)