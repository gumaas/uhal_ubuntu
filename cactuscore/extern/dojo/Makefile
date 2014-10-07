BUILD_HOME:=$(shell pwd)/../../..

include $(XDAQ_ROOT)/config/mfAutoconf.rules
include $(XDAQ_ROOT)/config/mfDefs.$(XDAQ_OS)

include $(BUILD_HOME)/config/Makefile.macros

Project = cactuscore
Package=extern/dojo
PackagePath = $(BUILD_HOME)/$(Project)/$(Package)
PackageName=cactuscore-extern-dojo

Packager = Ildefons Magrans de Abril, Marc Magrans de Abril

PACKAGE_VER_MAJOR = 0
PACKAGE_VER_MINOR = 4
PACKAGE_RELEASE = 10

TAR_NAME = dojo-0.4.0-widget
TAR_FILE = dojo-0.4.0-widget.tar.gz

RPMBUILD_DIR = ${PackagePath}/RPMBUILD

.PHONY: all _all clean _cleanall build _buildall rpm _rpmall

default: all

clean: _cleanall
_cleanall:
	rm -rf .build_done
	rm -rf $(RPMBUILD_DIR)
	rm -rf $(TAR_NAME)

default: _all
build: _all
all: _all
_all:
	if [ ! -f  .build_done ]; then   \
	tar -zxf $(TAR_FILE);                       \
	mkdir -p ${RPMBUILD_DIR}/{RPMS/{i386,i586,i686,x86_64},SPECS,BUILD,SOURCES,SRPMS};	\
	mkdir -p ${RPMBUILD_DIR}/SOURCES/htdocs/$(Package);    \
	cp -r $(TAR_NAME)/* ${RPMBUILD_DIR}/SOURCES/htdocs/$(Package) ;   \
	date > .build_done;   \
	fi;

_installall: install
install: all
	mkdir -p $(INSTALL_PREFIX)/$(XDAQ_PLATFORM)/htdocs
	rm -rf $(INSTALL_PREFIX)/$(XDAQ_PLATFORM)/htdocs/$(Package)
	cp -r ${RPMBUILD_DIR}/SOURCES/htdocs/$(Package) $(INSTALL_PREFIX)/$(XDAQ_PLATFORM)/htdocs

rpm: _rpmall
_rpmall: 
	rpmbuild -bb -bl --buildroot=${RPMBUILD_DIR}/BUILD				\
			--define  "_topdir ${RPMBUILD_DIR}"				\
			--define "_prefix ${XDAQ_ROOT}"   				\
			--define "tar_file ${TAR_FILE}"					\
			--define "sources_dir ${RPMBUILD_DIR}/SOURCES"			\
			--define "name ${PackageName}"					\
			--define "version ${PACKAGE_VER_MAJOR}.${PACKAGE_VER_MINOR}"	\
			--define "release ${PACKAGE_RELEASE}.${CACTUS_OS}"				\
			--define "packager ${Packager}"					\
			cactuscore-extern-dojo.spec

