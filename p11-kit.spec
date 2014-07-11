%define major	0
%define libname	%mklibname %{name} %{major}
%define devname	%mklibname %{name} -d

Summary:	Load and enumerate PKCS#11 modules
Name:		p11-kit
Version:	0.20.2
Release:	3
License:	Apache License
Group:		System/Libraries
Url:		http://p11-glue.freedesktop.org/p11-kit.html
Source0:	http://p11-glue.freedesktop.org/releases/%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:	pkgconfig(libffi)

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
%configure2_5x	--disable-static

%make

%install
%makeinstall_std

#dirs for configs etc
mkdir -p %{buildroot}%{_sysconfdir}/pkcs11/modules

#ghost files
touch %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf

%check
%make check

%post
%create_ghostfile %{_sysconfdir}/pkcs11/pkcs11.conf root root 644

%files
%doc AUTHORS NEWS
%{_bindir}/%{name}
%{_bindir}/trust
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%{_datadir}/%{name}/modules/%{name}-trust.module
%{_libdir}/pkcs11/%{name}-trust.so
%{_sysconfdir}/pkcs11/pkcs11.conf.example
%ghost %config(noreplace) %{_sysconfdir}/pkcs11/pkcs11.conf

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*
%{_libdir}/%{name}/trust-extract-compat

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/%{name}
%{_includedir}/%{name}-1
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-1.pc

