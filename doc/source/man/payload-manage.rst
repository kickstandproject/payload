==============
payload-manage
==============

--------------------------
Control and manage payload
--------------------------

:Author: paul.belanger@polybeacon.com
:Date: |today|
:Copyright: PolyBeacon, Inc
:Version: |version|
:Manual section: 1

SYNOPSIS
========

  payload-manage <category> <action> [<args>]

DESCRIPTION
===========

payload-manage is a CLI tool to control payload

OPTIONS
=======

 **General options**

payload DB
~~~~~~~~~~

``payload-manage db sync``

     Sync the database up to the most recent version.

``payload-manage db version``

     Print the current database version.

FILES
=====

* /etc/payload/payload.conf

SEE ALSO
========

* `payload <https://github.com/kickstandproject/payload>`__

BUGS
====

* payload is sourced in Github so you can view current bugs at `payload <https://github.com/kickstandproject/payload>`__
