%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	Load and enumerate PKCS#11 modules
Name:		p11-kit
Version:	0.23.12
Release:	3
License:	Apache License
Group:		System/Libraries
Url:		http://p11-glue.freedesktop.org/p11-kit.html
Source0:	https://github.com/p11-glue/p11-kit/archive/%{version}.tar.gz
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	rootcerts

%description
Provides a way to load and enumerate PKCS#11 modules. Provides a standard
configuration setup for installing PKCS#11 modules in such a way that
they're discoverable.

Also solves problems with coordinating the use of PKCS#11 by different
components or libraries living in the same process.

%package -n	%{libname}
Summary:	Library and proxy module for properly loading and sharing PKCS#11 modules
Group:		System/Libraries

%description -n	%{libname}
Provides a way to load and enumerate PKCS#11 modules. Provides a standard
configuration setup for installing PKCS#11 modules in such a way that
they're discoverable.

Also solves problems with coordinating the use of PKCS#11 by different
components or libraries living in the same process.

%package        trust
Summary:        System trust module from %{name}
Requires:	%{name} = %{version}-%{release}

%description    trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.

%package -n 	%{devname}
Summary:	Development files and headers for %{name}
Group:		Development/Other
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files and headers for %{name}.

%prep
%setup -q
%apply_patches

%build
%configure

%make

%install
%makeinstall_std

#dirs for configs etc
mkdir -p %{buildroot}%{_sysconfdir}/pkcs11/modules

# install the example config file as config file (mga #12696)
mv %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf.example %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf

%check
%make check

# remove invalid empty config file installed by default until p11-kit-0.20.1-3 (mga #12696)
%pretrans -p <lua>

file = io.open("/etc/pkcs11/pkcs11.conf","r")

if (file) then
  size = file:seek("end")
  file:close()
  if (size == 0) then
    os.remove("/etc/pkcs11/pkcs11.conf")
  end
end

%files
%doc p11-kit/pkcs11.conf.example
%{_bindir}/%{name}
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%config(noreplace) %{_sysconfdir}/pkcs11/pkcs11.conf
%dir %{_libdir}/p11-kit
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-1
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-1.pc

%files trust
%{_bindir}/trust
%dir %{_libdir}/pkcs11
%{_libdir}/pkcs11/p11-kit-trust.so
%{_libdir}/p11-kit/p11-kit-remote
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_libdir}/p11-kit/trust-extract-compat
