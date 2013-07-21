=============
stripe-manage
=============

-------------------------
Control and manage stripe
-------------------------

:Author: paul.belanger@polybeacon.com
:Date: |today|
:Copyright: PolyBeacon, Inc
:Version: |version|
:Manual section: 1

SYNOPSIS
========

  stripe-manage <category> <action> [<args>]

DESCRIPTION
===========

stripe-manage is a CLI tool to control stripe

OPTIONS
=======

 **General options**

Stripe DB
~~~~~~~~~

``stripe-manage db sync``

     Sync the database up to the most recent version.

``stripe-manage db version``

     Print the current database version.

FILES
========

* /etc/stripe/stripe.conf

SEE ALSO
========

* `Stripe <https://github.com/kickstandproject/stripe>`__

BUGS
====

* Stripe is sourced in Github so you can view current bugs at `Stripe <https://github.com/kickstandproject/stripe>`__
