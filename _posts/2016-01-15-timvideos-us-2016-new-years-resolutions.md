---
layout: "post"
title: "TimVideos.us 2016 New Year’s Resolutions"
date: "2016-01-15 01:00:58 +1000"
categories:
  - Lca
author: "mithro"
excerpt: "This is a cross post from the HDMI2USB website about my plans for 2016 and the TimVideos project. Last year was an exciting time for my personal projects! TimVideos.us 2016..."
wordpress_url: "https://blog.mithis.net/archives/lca/2167-timvideos-us-2016-new-years-resolutions"
---

<div class="entry-content">
<p>This is a <a href="https://hdmi2usb.tv/timvideos/hdmi2usb/2016/01/11/new-year-roadmap/">cross post</a> from the <a href="https://hdmi2usb.tv">HDMI2USB</a> website about my plans for 2016 and the <a href="https://code.timvideos.us/">TimVideos project</a>. Last year was an exciting time for my personal projects!</p>
<blockquote>
<h1><a href="https://hdmi2usb.tv/timvideos/hdmi2usb/2016/01/11/new-year-roadmap/">TimVideos.us 2016 New Year’s Resolutions</a></h1>
<hr/>
<p>Hello everyone,</p>
<p>Hope everyone has had an awesome start to 2016 so far. As is tradition in many western countries, I thought I would put together some <a href="https://en.wikipedia.org/wiki/New_Year%27s_resolution">New Year’s Resolutions</a> and reflect on our progress in 2015. I guess more business minded people might call it a “project roadmap” 🙂</p>
<h3 id="timvideos-project"><a href="https://code.timvideos.us/">TimVideos Project</a></h3>
<p>In 2015, I decided to focus the <a href="https://code.timvideos.us/">TimVideos project</a> on the <a href="https://hdmi2usb.tv/">HDMI2USB project</a>. The three key results of this focus were;</p>
<ul>
<li>Starting and completing a <a href="https://github.com/timvideos/HDMI2USB-misoc-firmware">rewrite of the HDMI2USB firmware</a> based on the <a href="http://m-labs.hk/gateware.html">Migen and MiSoC system developed by M-Labs</a>.</li>
<li>Launching a <a href="http://crowdsupply.com/numato-lab/opsis">successful crowdfunding campaign</a> for <a href="https://github.com/timvideos/HDMI2USB-numato-opsis-hardware">Numato Opsis</a>, our first open hardware for the HDMI2USB firmware.</li>
<li>Having the HDMI2USB firmware on Atlys boards used in production by multiple people!
<ul>
<li>Carl Karsten from <a href="http://nextdayvideo.com/">NextDayVideo</a> in the US for both PyCon ZA and Nodevember.</li>
<li>The <a href="https://wiki.debconf.org/wiki/Videoteam">DebConf Video team</a> for their <a href="https://wiki.debian.org/DebianEvents/gb/2015/MiniDebConfCambridge#Video">MiniDebConf in November</a>.</li>
<li><a href="https://www.youtube.com/user/mithro">Myself for recording</a> my own talks on the HDMI2USB project at user groups here in Sydney!</li>
</ul>
</li>
</ul>
<p>With the success of this focus in 2015, the <a href="https://code.timvideos.us/">TimVideos project</a> is going to continue to focus on the<a href="https://hdmi2usb.tv/">HDMI2USB project</a> for 2016 (and I’ll go into more detailed goals shortly).</p>
<p>The <a href="https://code.timvideos.us/">TimVideos project</a> has also been mildly successful in collaborating with other open source groups doing things related to video recording and production. In 2016, I hope we can strengthen these bonds and forge new ones. Some specific goals around this include;</p>
<ul>
<li>Getting the TimVideos project to join <a href="https://sfconservancy.org/">Software Freedom Conservancy</a> (or similar organisation).</li>
<li>Figure out the right way to collaborate with the <a href="https://c3voc.de/">C3VOC team</a> on <a href="https://github.com/voc/voctomix">voctomix</a> and start adding missing features from <a href="https://github.com/timvideos/gst-switch">gst-switch</a> allowing that project to be retired.</li>
<li>Continue to work with supporting groups like <a href="http://nextdayvideo.com/">NextDayVideo</a>, the <a href="https://wiki.debconf.org/wiki/Videoteam">DebConf Video team</a> and <a href="https://linux.org.au/">Linux Australia</a>.</li>
<li>Support and help <a href="http://hamsterworks.co.nz/mediawiki/index.php/FPGA_Projects">Mike “Hamster” Field</a> continue to develop a <a href="https://github.com/hamsternz/FPGA_DisplayPort">fully open source DisplayPort core</a>.</li>
<li>Collaborate with the <a href="http://apertus.org/">apertus° project</a> on high end (4k and greater!) video capture and processing.</li>
</ul>
<h3 id="hdmi2usb-project"><a href="https://hdmi2usb.tv">HDMI2USB Project</a></h3>
<p>As we are concentrating on the <a href="https://hdmi2usb.tv">HDMI2USB project</a>, we have some specific goals around that.</p>
<p>HDMI2USB <strong>firmware</strong> goals;</p>
<ul>
<li>Refactor the HDMI core to allow support a wider range of interfaces, better debugging and addition of more features. A document about the refactor has been <a href="https://docs.google.com/a/mithis.com/document/d/1L8lz7u2uj6MrzSQv4b1Vk6Rmic26okyRklOju5IWLYA/edit?usp=drive_web">started here</a>.</li>
<li>Add support for the <a href="https://hdmi2usb.tv/timvideos/hdmi2usb/2016/01/11/new-year-roadmap/">high-speed GTP transceivers</a> and <a href="http://hamsterworks.co.nz/mediawiki/index.php/FPGA_Projects">Mike “Hamster” Field</a> <a href="https://github.com/hamsternz/FPGA_DisplayPort">open source DisplayPort core</a>.</li>
<li>Get Ethernet support working (on both the Atlys and Opsis boards). The two major Ethernet features are;
<ul>
<li>Ethernet supports identical capture and control feature set to the USB port.</li>
<li>Allowing HDMI2USB boards to act has “HDMI over Ethernet extenders”.</li>
</ul>
</li>
<li><a href="https://hdmi2usb.tv/potential-boards/">Support for more hardware</a>;
<ul>
<li>miniSpartan6+</li>
<li>Digilent Nexys Video</li>
<li>New HDMI2USB designed hardware!</li>
</ul>
</li>
<li>Stretch Goals (1)
<ul>
<li>Add support for <a href="https://docs.google.com/document/d/1ZjM1Brrks0lg1CJp2Rt1BH8-MhJamrKUeCUB4s4nzoA/edit">hardware based mixing</a>.</li>
<li>Have either a RTOS or Linux running on the FPGA softcore.</li>
</ul>
</li>
</ul>
<p>HDMI2USB <strong>hardware</strong> goals;</p>
<ul>
<li>(By end of year) Development of a low cost PCI-Express capture card.</li>
<li>(By middle 2017) Development of an Opsis V2 based around either an high end Artix-7 or a low end Kintex-7 FPGA.</li>
</ul>
<p><em>(1): Stretch goals are things we plan to try and achieve if things go well.</em></p>
<p>Hope this update give you an idea of what we have planned for 2016! We would love your help making it all possible.</p>
<p>Tim ‘mithro’ Ansell</p></blockquote>
</div>