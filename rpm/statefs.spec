Summary: Syntetic filesystem to expose system state
Name: statefs
Version: 0.2.7
Release: 1
License: LGPLv2
Group: System Environment/Tools
URL: http://github.com/nemomobile/statefs
Source0: %{name}-%{version}.tar.bz2
BuildRequires: pkgconfig(fuse)
BuildRequires: boost-filesystem
BuildRequires: boost-devel
BuildRequires: cmake >= 2.8
BuildRequires: doxygen
BuildRequires: pkgconfig(cor) >= 0.1.2
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(QtXml)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: contextkit-devel

%description
StateFS is the syntetic filesystem to expose current system state
provided by StateFS plugins as properties wrapped into namespaces.

%package provider-devel
Summary: Files to develop statefs providers
Group: System Environment/Libraries
%description provider-devel
Headers, libraries etc. needed to develop statefs providers

%package provider-doc
Summary: Statefs provider developer documentation
Group: System Environment/Libraries
%description provider-doc
Statefs provider developer documentation

%package -n statefs-contextkit-provider
Summary: Provider to expose contextkit providers properties
Group: System Environment/Libraries
Requires: statefs
%description -n statefs-contextkit-provider
Provider exposes all contextkit providers properties

%package -n statefs-contextkit-subscriber-qt4
Summary: Contextkit property interface using statefs
Group: System Environment/Libraries
Requires: statefs
%description -n statefs-contextkit-subscriber-qt4
Contextkit property interface using statefs instead of contextkit

%package -n statefs-contextkit-subscriber-qt4-devel
Summary: Contextkit property interface using statefs
Group: System Environment/Libraries
Requires: statefs-contextkit-subscriber-qt4
%description -n statefs-contextkit-subscriber-qt4-devel
Contextkit property interface using statefs instead of contextkit

%package -n statefs-contextkit-subscriber
Summary: Contextkit property interface using statefs
Group: System Environment/Libraries
Requires: statefs
%description -n statefs-contextkit-subscriber
Contextkit property interface using statefs instead of contextkit

%package -n statefs-contextkit-subscriber-devel
Summary: Contextkit property interface using statefs
Group: System Environment/Libraries
Requires: statefs-contextkit-subscriber
%description -n statefs-contextkit-subscriber-devel
Contextkit property interface using statefs instead of contextkit

%prep
%setup -q

%build
%cmake -DUSEQT=4
make %{?jobs:-j%jobs}
make provider-doc
%cmake -DUSEQT=5
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%cmake -DUSEQT=4
make install DESTDIR=%{buildroot}
%cmake -DUSEQT=5
make install DESTDIR=%{buildroot}
install -D -p -m644 packaging/statefs.service %{buildroot}%{_unitdir}/statefs.service
install -d -D -p -m755 %{buildroot}%{_sharedstatedir}/statefs
install -d -D -p -m755 %{buildroot}%{_datarootdir}/doc/statefs/html
cp -R doc/html/ %{buildroot}%{_datarootdir}/doc/statefs/
install -d -D -p -m755 %{buildroot}%{_sharedstatedir}/doc/statefs/html

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/statefs
%{_bindir}/statefs-prerun
%{_sharedstatedir}/statefs
%{_unitdir}/statefs.service

%files provider-devel
%defattr(-,root,root,-)
%{_includedir}/statefs/*.h
%{_libdir}/pkgconfig/statefs.pc

%files provider-doc
%defattr(-,root,root,-)
%{_datarootdir}/doc/statefs/html/*

%files -n statefs-contextkit-provider
%defattr(-,root,root,-)
%{_libdir}/libstatefs-provider-contextkit.so

%files -n statefs-contextkit-subscriber-qt4
%defattr(-,root,root,-)
%{_libdir}/libcontextkit-statefs-qt4.so

%files -n statefs-contextkit-subscriber-qt4-devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/contextkit-statefs-qt4.pc

%files -n statefs-contextkit-subscriber
%defattr(-,root,root,-)
%{_libdir}/libcontextkit-statefs.so

%files -n statefs-contextkit-subscriber-devel
%defattr(-,root,root,-)
%{_includedir}/contextproperty.h
%{_libdir}/pkgconfig/contextkit-statefs.pc

%post
systemctl enable statefs.service
systemctl start statefs.service

%preun
systemctl stop statefs.service
systemctl disable statefs.service

%post -n statefs-contextkit-provider
statefs register %{_libdir}/libstatefs-provider-contextkit.so

