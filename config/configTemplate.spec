%define _package __package__
%define _packagename __packagename__
%define _version __version__
%define _release __release__
%define _prefix  __prefix__
%define _sources_dir __sources_dir__
%define _tmppath /tmp
%define _packagedir __packagedir__
%define _os __os__
%define _platform __platform__
%define _project __project__
%define _author __author__
%define _summary __summary__
%define _url __url__

Name: %{_packagename}
Version: %{_version}
Release: %{_release}
Packager: %{_author}
Summary: %{_summary}
License: BSD License
Group: CACTUS
Source: %{_source}
URL: %{_url}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

%description
__description__

%prep

%build
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/config
install -m 655 %{_packagedir}/Makefile $RPM_BUILD_ROOT/%{_prefix}/config
install -m 655 %{_packagedir}/*.spec $RPM_BUILD_ROOT/%{_prefix}/config
install -m 655 %{_packagedir}/*.macros $RPM_BUILD_ROOT/%{_prefix}/config
# For the future
# install -m 655 %{_packagedir}/*.mk $RPM_BUILD_ROOT/%{_prefix}/config

%clean

%post

%postun

#
# Files that go in the binary RPM
#
%files
%defattr(-,root,root,-)

%dir
%{_prefix}/config