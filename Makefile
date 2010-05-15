PKGNAME=apache-activemq
PKGVERSION=$(shell grep '%global amqversion' ${PKGNAME}.spec | awk '{print $$3}')

TGZREPO=http://www.apache.org/dist/activemq/${PKGNAME}/${PKGVERSION}

BUILD=${shell pwd}/build
SOURCEFILES := $(shell cat sources 2>/dev/null | awk '{ print $$2 }')

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
	cp activemq-conf  activemq.initd ${PKGNAME}-${PKGVERSION}-bin.tar.gz build/SOURCES 

rpm: prepare
	@rpmbuild -ba --define='_topdir $(BUILD)' $(PKGNAME).spec

clean:
	@for F in $(SOURCEFILES) ; do \
	  rm -f $$F ; \
	done

