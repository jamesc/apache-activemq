%define debug_package %{nil}

%global amqversion 5.3.2
# If this is a snapshot, put the date here
#global snapshot_version 100507



# This is the version of ActiveMQ, but in a form acceptable
# an an RPM version string (i.e. no '-')
%global rpmversion %(echo %{amqversion} | tr '-' '_')
%global pkgversion %{amqversion}%{?snapshot_version:-SNAPSHOT}

Name:           apache-activemq
Version:        %{rpmversion}%{?snapshot_version:_SNAPSHOT} 
Epoch:          1
Release:        1%{?snapshot_version:.%{snapshot_version}}%{?dist}
Summary:        ActiveMQ Messaging Broker

Group:          System    
License:        Apache License
URL:            http://activemq.apache.org/
Source0: %{?snapshot_version:https://repository.apache.org/content/repositories/snapshots/org/apache/activemq/%{name}/%{pkgversion}/%{name}-%{pkgversion}-bin.tar.gz}%{!?snapshot_version:http://www.apache.org/dist/activemq/%{name}/%{pkgversion}/%{name}-%{pkgversion}-bin.tar.gz}
Source1:        activemq-conf
Patch0:         init.d.patch
Patch1:         wrapper.conf.patch
Patch2:         log4j.patch
BuildRoot:      %{_tmppath}/%{name}-%{pkgversion}-%{release}-root-%(%{__id_u} -n)

%define amqhome /usr/share/activemq

%if  %{_arch} == i386
%define amqarch 32
%define amqother 64
%endif

%if  %{_arch} == x86_64
%define amqarch 64
%define amqother 32
%endif

%package client
Summary: Client jar for Apache ActiveMQ
Group:       System
%description client
Client jar for Apache ActiveMQ

%description


%prep
%setup -q -n apache-activemq-%{pkgversion}
%patch0 -p1
%patch1 -p1
%patch2 -p1


%build
/bin/true

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{amqhome}
mv * $RPM_BUILD_ROOT%{amqhome}

pushd $RPM_BUILD_ROOT%{amqhome}/bin
  ln -s linux-x86-%{amqarch} linux
popd

mkdir -p $RPM_BUILD_ROOT/usr/bin
pushd $RPM_BUILD_ROOT/usr/bin
    ln -s %{amqhome}/bin/activemq-admin activemq-admin
    ln -s %{amqhome}/bin/activemq activemq
popd

mkdir -p $RPM_BUILD_ROOT/etc
mv $RPM_BUILD_ROOT%{amqhome}/conf $RPM_BUILD_ROOT/etc/activemq
pushd $RPM_BUILD_ROOT%{amqhome}
  ln -s /etc/activemq conf
popd
mkdir -p $RPM_BUILD_ROOT/etc/init.d

mkdir -p $RPM_BUILD_ROOT/var/log/activemq
pushd $RPM_BUILD_ROOT%{amqhome}
  ln -s /var/log/activemq log
popd

mkdir -p $RPM_BUILD_ROOT/var/run/activemq
mkdir -p $RPM_BUILD_ROOT/var/cache/activemq/data
# this shuld be blank - it comes with an empty logfile
rm -rf $RPM_BUILD_ROOT/%{amqhome}/data
pushd $RPM_BUILD_ROOT%{amqhome}
  ln -s /var/cache/activemq/data data
popd

mkdir -p $RPM_BUILD_ROOT%{_javadir}
mv $RPM_BUILD_ROOT%{amqhome}/activemq-all-%{pkgversion}.jar \
    $RPM_BUILD_ROOT%{_javadir}/activemq-all-%{pkgversion}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{pkgversion}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{pkgversion}||g"`; done)

install -D -m 0644 %{SOURCE1}  $RPM_BUILD_ROOT/etc/activemq.conf

rm -rf $RPM_BUILD_ROOT%{amqhome}/bin/linux-x86-%{amqother} 
rm -rf $RPM_BUILD_ROOT%{amqhome}/bin/macosx
mv $RPM_BUILD_ROOT%{amqhome}/bin/linux-x86-%{amqarch}/wrapper.conf $RPM_BUILD_ROOT/etc/activemq
mv $RPM_BUILD_ROOT%{amqhome}/bin/linux-x86-%{amqarch}/activemq $RPM_BUILD_ROOT/etc/init.d

%clean
rm -rf $RPM_BUILD_ROOT


%pre
# Add the "activemq" user and group
# we need a shell to be able to use su - later
/usr/sbin/groupadd -g 92 -r activemq 2> /dev/null || :
/usr/sbin/useradd -c "Apache Activemq" -u 92 -g activemq \
    -s /bin/bash -r -d /usr/share/activemq activemq 2> /dev/null || :

%post
# install activemq (but don't activate)
/sbin/chkconfig --add activemq

%preun
if [ $1 = 0 ]; then
    [ -f /var/lock/subsys/activemq ] && /etc/init.d/activemq stop
    [ -f /etc/init.d/activemq ] && /sbin/chkconfig --del activemq
fi




%files
%defattr(-,root,root,-)
%{amqhome}*
%attr(0755,root,root) /etc/init.d/activemq
%attr(0755,root,root) /usr/bin/activemq
%attr(0755,root,root) /usr/bin/activemq-admin
%config(noreplace)    /etc/activemq.conf

%config(noreplace) /etc/activemq/*
%attr(775,activemq,activemq) %dir /var/log/activemq
%attr(775,activemq,activemq) %dir /var/run/activemq
%attr(775,root,activemq)     %dir /var/cache/activemq/data

%files client
%{_javadir}

%changelog
* Fri May 07 2010 James Casey <james.casey@cern.ch> - 5.3.1-1
- First version of specfile
