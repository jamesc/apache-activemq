Introduction
------------
This is a makefile and a set of patches to buld Apache ActiveMQ from
a binary tarball.  It includes pulling the tarball from the Apache dist
webserver (sources target) and also building the rpm (rpm target).

The patches are all small, and are either already submitted upstream or
are things only really relevant to the RPM distribution (change of default
directories for config files and log files).

Moving to a new version
-----------------------
The only changes needed when moving to a new version is to modify the `amqversion`
in the specfile and changing the `sources` file to contain the new filename and
MD5 checksum of upstream tarball.

Building a SNAPSHOT
-------------------
The rpm also support building a SNAPSHOT rpm directly from the SNAPSHOT 
repository.  To build a snapshot, edit `apache-activemq.spec` and change the line:

    #global snapshot_version 100507

to something like

    %global snapshot_version YYMMDD

where `YYMMDD` is the current date.  You also need to change the `Makefile` to point at
the right filename (with thr right checksum.


This will produce an rpm with the 
name similar to  `apache-activemq-5.3.2_SNAPSHOT-1.YYMMDD`.
