---
author: mithro
categories:
- Uncategorized
date: 2008-07-08T14:43:04+1000
excerpt: Recovered from Wayback Machine archive
layout: post
permalink: /archives/uncategorized/87-babylon-5-dvd-copy-protection
title: Babylon 5, the adventure with DVD copy protection
wayback_recovered: true
wordpress_category: uncategorized
wordpress_id: 87
wordpress_url: https://blog.mithis.net/archives/uncategorized/87-babylon-5-dvd-copy-protection
---

<div >
<p>I still have not found an apartment so as I have no internet to entertain me on the weekend I got a copy of the first season of <a href="http://en.wikipedia.org/wiki/Babylon_5" title="Babylon 5">Babylon 5</a> (it was only $20.00 AUD for the whole season). I had been working my way through <a href="http://en.wikipedia.org/wiki/Andromeda_(TV_series)" title="Gene Roddenberry's Andromeda">Andromeda</a> but no where seems to have the third season.</p>
<p>Anyway when I put the DVD video in the drive in my Sony Vaio Laptop running Ubuntu Hardy all I got where I/O errors, some examples are below;</p>
<blockquote><p>[ 2283.614887] end_request: I/O error, dev sr0, sector 418256<br/>
[ 2283.620351] end_request: I/O error, dev sr0, sector 418264<br/>
[ 2283.626273] end_request: I/O error, dev sr0, sector 418264<br/>
[ 2283.631766] end_request: I/O error, dev sr0, sector 418272<br/>
[ 2283.637013] end_request: I/O error, dev sr0, sector 418272<br/>
[ 2283.642384] end_request: I/O error, dev sr0, sector 418280</p></blockquote>
<p>The Vaio’s DVD drive is connected via the USB bus. This is done so that drive can be completely powered down. The device turned out to be a MATSHITA DVD-RAM drive as shown via the dmesg output below;</p>
<blockquote><p>[ 2909.596251] scsi11 : SCSI emulation for USB Mass Storage devices<br/>
[ 2909.596944] usb-storage: device found at 24<br/>
[ 2909.596952] usb-storage: waiting for device to settle before scanning<br/>
[ 2911.901103] usb-storage: device scan complete<br/>
[ 2911.903506] scsi 11:0:0:0: CD-ROMÂ Â Â Â Â Â Â Â Â Â Â  MATSHITA DVD-RAM UJ-852SÂ  1.31 PQ: 0 ANSI: 0<br/>
[ 2911.948247] sr1: scsi3-mmc drive: 24x/24x writer dvd-ram cd/rw xa/form2 cdda tray<br/>
[ 2911.948372] sr 11:0:0:0: Attached scsi CD-ROM sr1<br/>
[ 2911.948460] sr 11:0:0:0: Attached scsi generic sg1 type 5</p></blockquote>
<p>It took me forever to figure out what was going on. I had seen similar problems on my desktop before when the disk was scratched but these where brand new disks. So I took the disks into work and tested it out on a friends Mac, it played perfectly. There happened to be a Steve Irwin DVD video disk lying around, so I popped it in the Vaio, it also played perfectly! What was going on?</p>
<p>After much searching I came across some reference to problems with region coding. It turns out thatÂ  MATSHITA drives won’t let you read a dvd unless they they have a region set. As I had never played a DVD video before the region on the drive had never been set.</p>
<p>There is a tool in Linux which can be used to do the region setting, it is helpfully called regionset. After setting the region to “Region 4″ I am now able to play my new DVDs! I wonder if I will be able to read my discs from the US and the UK. The libdvdcss2 should be able to decode the data if it can be read, hopefully the drive will still let that occurring. I will report back in comments here when I find out for sure.</p>
<p>It has been repetitively found that region encoding is anticompetitive and hence un-unenforceable in Australia. I have included a quote from the <a href="http://www.austlii.edu.au/au/cases/cth/high_ct/2005/58.html"><em>Stevens v Kabushiki Kaisha Sony Computer Entertainment</em> case from 2005</a><em>.<br/>
</em></p>
<blockquote><p>Ordinary principles of statutory construction, observed by this Court since its earliest days, have construed legislation, where there is doubt, to protect the fundamental rights of the individual<a href="http://www.austlii.edu.au/au/cases/cth/high_ct/2005/58.html#fn159" name="fnB159"></a>. The right of the individual to enjoy lawfully acquired private property (a CD ROM game or a PlayStation console purchased in another region of the world or possibly to make a backup copy of the CD ROM) would ordinarily be a right inherent in Australian law upon the acquisition of such a chattel. This is a further reason why sÂ 116A of the <a  href="http://www.austlii.edu.au/au/legis/cth/consol_act/ca1968133/">Copyright Act</a> and the definition of TPM in <a  href="http://www.austlii.edu.au/au/legis/cth/consol_act/ca1968133/s10.html">sÂ 10(1)</a> of that Act should be read strictly. Doing so avoids an interpretation that would deprive the property owner of an incident of that person’s ordinary legal rights.</p></blockquote>
<p>I thought I would just log my info here as there was very little information in Google about this problem. Hopefully I help some poor fool which brought a Sony Vaio like me.</p>
</div>