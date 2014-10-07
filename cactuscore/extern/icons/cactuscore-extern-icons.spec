#
# spefile for PugiXML
#
Name: %{name} 
Version: %{version} 
Release: %{release} 
Packager: %{packager}
Summary: Icons for the Trigger Supervisor
License: BSD
Group: trigger
Source: %{tar_file}
URL:  https://svnweb.cern.ch/trac/cactus/browser/trunk/trigger/extern/icons
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot 
Prefix: %{_prefix}

%description
Icons for the Trigger Supervisor

%prep

%build


%install 

# copy includes to RPM_BUILD_ROOT and set aliases
mkdir -p $RPM_BUILD_ROOT%{_prefix}/htdocs
cp -rp %{sources_dir}/htdocs/* $RPM_BUILD_ROOT%{_prefix}/htdocs/.

#Change access rights
chmod -R 755 $RPM_BUILD_ROOT%{_prefix}/htdocs

%clean 

%post 

%postun 

%files 
%defattr(-, root, root) 
%{_prefix}/htdocs/*

