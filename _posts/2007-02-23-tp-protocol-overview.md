---
author: mithro
categories:
- tp
date: 2007-02-23T01:21:13+1000
excerpt: "I've been planning to try and get tp04 into draft stage for a while now.\
  \ However the AI competition and RL has kept me really busy so I haven't got time\
  \ to do the draft yet...."
layout: post
permalink: /archives/tp/15-tp-protocol-overview
title: Thousand Parsec Protocol Overview
wordpress_category: tp
wordpress_id: 15
wordpress_url: https://blog.mithis.net/archives/tp/15-tp-protocol-overview
---
I've been planning to try and get tp04 into draft stage for a while now. However the AI competition and RL has kept me really busy so I haven't got time to do the draft yet. I am going to however go over some highlights of the new tp04 protocol.

Firstly, what does tp03 currently have?

Dynamic Orders
: Thousand Parsec servers can define new orders and clients can automatically discover these orders and show the user quite a bit of detail about what arguments should be given to the order.

Comprehensive Design Support with tpcl
: Designing things is a very important part of most empire building games. tp03 includes support for building designs out of "components", these components dynamical describe their properties and requirements. They can be either calculated on the server or calculated on the client. It is quite possible to have components which require other components, forbid other components via either specific exclusion or by using property values.

Dynamic Resources
: Resources which are used for doing things are dynamical described by the server.

Message and Board system
: Support for a wide variety of messages including referencing objects related to a message (IE This message came from this object). Servers can also have both private and public boards.

Partial Design Discover
: Although no server currently implements a system where as you can only discover partial information about enemy designs, this option is total supported.

The next version of the tp protocol tp04 will have a bunch of new features. It is going to be built in an incremental way based on tp03. All the highlights of tp03 will still exist in tp04.

Some of the new highlights include.

Full XML protocol specification
: The protocol will be completely specified in an XML document. This will allow more dynamic languages (such as Python, Ruby and PHP) to read in the protocol document and dynamical create the correct data. This doesn't mean our good documentation is going away (for those people who want to implement it the "hard way"), instead it will be more accurate and contain better linking, lot more useful tables and even an index. The documentation will all be generated using XSLT from the protocol XML document so it will also always be current.

Meta Protocol definition
: A definition on how to talk the "meta protocol", IE talking to the metaserver and find local games will be specified. It will be almost identical to the current protocol specified separately.

Filter Support
: The protocol will support filters such as encryption and compression (or even a 32bit aligned strings filter), there will be a way to negotiate which filters to use.

Difference Support
: The protocol will include (and servers will be required to support) a proper method for downloading "what has changed" lists. This will be extended from the current "get id sequence" stuff but made so it doesn't require downloading every single ID in the universe to find out the differences.

Dynamic Objects
: Like how servers can define new a interesting order types, with tp04 servers will also be able to do the same for objects. A wide variety of object properties types will exist, from Graph like properties to just plain strings. This will rapidly allow many more advanced rulesets to exist.

    Old Data support
    : As a side effect of Dynamic Objects, object properties will be able to be "aged". This means that if you could detect/determine the value in the past, but can't determine the value now, the client will be able to understand this.

    Multiple Instruction queue support
    : As another side effect of Dynamic Objects, objects will be able to have multiple instruction queues. These will allow for things like "standing battle orders" and "research queues" (and probably plenty of other things I can't think of at this very moment).

    Media support
    : The current "media support" is just a hack in tpclient-pywx. The dynamic objects will allow proper specification of what media should be used for objects and such.

Research support
: The protocol will include support for figuring out which "Research options" are available. It will support a wide range of research methods too (from researching for a specific object, to researching in a general area).

EOT Support
: There will be support for things like saying "I'm Done" and "Please end the turn now.". This will mean we are no longer just stuck with the EOT at a certain time problem like in tpserver-cpp (or when admin runs a special program like in tpserver-py).

Frame Type Versions
: Support for changing frames (in a backward compatible way) separately. This will allow better updates of the protocol without having to do a complete new version.

tp05 will very much be another incremental version on top of tp04, the following is a list of what is planned for tp05 (and will not be included in tp04).

History Support
: Servers should start worrying about storing history as it will definitely be added in tp05.

Trading or Diplomacy
: Diplomacy will still be able to be done via sending messages to each other, however the server will not support guaranteed diplomacy and trading. (IE If a person says they won't attack you, the server will have no knowledge of this and they could still attack you.)

Player / Race Separation
: There will be no specific support for a player controlling multiple races or a race having multiple players until tp05.

Other stuff?
: Probably plenty of other stuff which I have forgotten.
