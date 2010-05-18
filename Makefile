SPECNAME=activemq
PKGNAME=apache-activemq
AMQVERSION=$(shell grep '%global amqversion' ${SPECNAME}.spec | awk '{print $$3}')
SNAPSHOT= $(shell grep '^%global snapshot_version' ${SPECNAME}.spec | cut -f3 -d' ' )


ifeq (${SNAPSHOT},)
	PKGVERSION=${AMQVERSION}
	TGZREPO=http://www.apache.org/dist/activemq/${PKGNAME}/${PKGVERSION}
else
	PKGVERSION=${AMQVERSION}-SNAPSHOT
	TGZREPO=https://repository.apache.org/content/repositories/snapshots/org/apache/activemq/${PKGNAME}/${PKGVERSION}
endif

BUILD=${shell pwd}/build
PATCHFILES := $(shell ls *.patch)
SOURCEFILES := $(shell cat sources 2>/dev/null | awk '{ print $$2 }')

all: rpm

sources: $(SOURCEFILES) 

$(SOURCEFILES):
	@echo "Downloading $(TGZREPO)/$@..."
	curl -H Pragma -O -R -S --fail --show-error $(TGZREPO)/$@

prepare: sources
	@mkdir -p  build/RPMS/noarch
	@mkdir -p  build/SRPMS/
	@mkdir -p  build/SPECS/
	@mkdir -p  build/SOURCES/
	@mkdir -p  build/BUILD/
	cp activemq-conf $(PATCHFILES) ${PKGNAME}-${PKGVERSION}-bin.tar.gz build/SOURCES 

rpm: prepare
	@rpmbuild -ba --define='_topdir $(BUILD)' $(SPECNAME).spec

clean:
	@for F in $(SOURCEFILES) ; do \
	  rm -f $$F ; \
	done
	@rm -rf $(BUILD)

