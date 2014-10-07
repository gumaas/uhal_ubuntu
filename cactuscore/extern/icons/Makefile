BUILD_HOME:=$(shell pwd)/../../..

include $(XDAQ_ROOT)/config/mfAutoconf.rules
include $(XDAQ_ROOT)/config/mfDefs.$(XDAQ_OS)

include $(BUILD_HOME)/config/Makefile.macros

Project = cactuscore
Package = extern/icons
PackagePath = $(BUILD_HOME)/$(Project)/$(Package)
PackageName=cactuscore-extern-icons

Packager = Marc Magrans de Abril

PACKAGE_VER_MAJOR = 0
PACKAGE_VER_MINOR = 1
PACKAGE_RELEASE = 12

TAR_NAME = icons
TAR_FILE = icons.tar.gz

RPMBUILD_DIR = ${PackagePath}/RPMBUILD

.PHONY: all _all clean _cleanall build _buildall rpm _rpmall

default: all

clean: _cleanall
_cleanall:
	rm -rf $(RPMBUILD_DIR)
	rm -rf $(TAR_NAME)

default: _all
build: _all
all: _all
_all:
	if [ ! -f  $(TAR_NAME)/.build_done ]; then   \
	tar -zxf $(TAR_FILE);                       \
	mkdir -p ${RPMBUILD_DIR}/{RPMS/{i386,i586,i686,x86_64},SPECS,BUILD,SOURCES,SRPMS};	\
	mkdir -p ${RPMBUILD_DIR}/SOURCES/htdocs/$(Package);    \
	cp icons/* ${RPMBUILD_DIR}/SOURCES/htdocs/$(Package)/. ;   \
	date > $(TAR_NAME)/.build_done;   \
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
			--define "_prefix ${XDAQ_ROOT}"					\
			--define "tar_file ${TAR_FILE}"					\
			--define "sources_dir ${RPMBUILD_DIR}/SOURCES"			\
			--define "name ${PackageName}"					\
			--define "version ${PACKAGE_VER_MAJOR}.${PACKAGE_VER_MINOR}"	\
			--define "release ${PACKAGE_RELEASE}.${CACTUS_OS}"				\
			--define "packager ${Packager}"					\
			cactuscore-extern-icons.spec

