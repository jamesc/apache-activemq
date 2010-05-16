Introduction
------------
This is a makefile and a set of patches to buld Apache ActiveMQ from
a binary tarball.  It includes pulling the tarball from the Apache dist
webserver (sources target) and also building the rpm (rpm target).

The patches are all small, and are either already submitted upstream or
are things only really relevant to the RPM distribution (change of default
directories for config files and log files).

Building a SNAPSHOT
-------------------
The rpm also support building a SNAPSHOT rpm directly from the SNAPSHOT 
repository.  To build a snapshot, edit `apache-activemq.spec` and

