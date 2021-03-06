%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Load and enumerate PKCS#11 modules
Name:		p11-kit
Version:	0.23.22
Release:	1
License:	Apache License
Group:		System/Libraries
Url:		http://p11-glue.freedesktop.org/p11-kit.html
Source0:	https://github.com/p11-glue/p11-kit/archive/%{version}.tar.xz
Patch0:		https://src.fedoraproject.org/rpms/p11-kit/raw/rawhide/f/p11-kit-0.23.22-progname-leak.patch
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(libtasn1)
BuildRequires:	pkgconfig(libffi)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	systemd-macros
BuildRequires:	libtasn1-tools
BuildRequires:	rootcerts
BuildRequires:	meson

%description
Provides a way to load and enumerate PKCS#11 modules. Provides a standard
configuration setup for installing PKCS#11 modules in such a way that
they're discoverable.

Also solves problems with coordinating the use of PKCS#11 by different
components or libraries living in the same process.

%package -n %{libname}
Summary:	Library and proxy module for properly loading and sharing PKCS#11 modules
Group:		System/Libraries

%description -n %{libname}
Provides a way to load and enumerate PKCS#11 modules. Provides a standard
configuration setup for installing PKCS#11 modules in such a way that
they're discoverable.

Also solves problems with coordinating the use of PKCS#11 by different
components or libraries living in the same process.

%package trust
Summary:	System trust module from %{name}
Requires:	%{name} = %{EVRD}

%description    trust
The %{name}-trust package contains a system trust PKCS#11 module which
contains certificate anchors and black lists.

%package -n %{devname}
Summary:	Development files and headers for %{name}
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains the development files and headers for %{name}.

%prep
%autosetup -p1

%build
%meson -Dtrust_paths=%{_sysconfdir}/pki/ca-trust/source:%{_datadir}/pki/ca-trust-source
%meson_build

%install
%meson_install

#dirs for configs etc
mkdir -p %{buildroot}%{_sysconfdir}/pkcs11/modules

# install the example config file as config file (mga #12696)
cp build/p11-kit/pkcs11.conf.example %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf
rm -f %{buildroot}%{_sysconfdir}/pkcs11/pkcs11.conf.example

# (tpg) enable p11-kit-server.socket in userland
mkdir -p %{buildroot}%{_userunitdir}/sockets.target.wants
ln -sf %{_userunitdir}/p11-kit-server.socket %{buildroot}%{_userunitdir}/sockets.target.wants/p11-kit-server.socket

%find_lang %{name}

%check
meson test -C build

# remove invalid empty config file installed by default until p11-kit-0.20.1-3 (mga #12696)
%triggerin -p <lua> -- %{name} < 0.23.15
file = io.open("/etc/pkcs11/pkcs11.conf","r")

if (file) then
  size = file:seek("end")
  file:close()
  if (size == 0) then
    os.remove("/etc/pkcs11/pkcs11.conf")
  end
end

%files -f %%{name}.lang
%{_bindir}/%{name}
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%config(noreplace) %{_sysconfdir}/pkcs11/pkcs11.conf
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%dir %{_libexecdir}/p11-kit
%dir %{_libdir}/pkcs11
%{_libexecdir}/p11-kit/p11-kit-remote
%{_libexecdir}/p11-kit/p11-kit-server
%{_userunitdir}/p11-kit-server.service
%{_userunitdir}/p11-kit-server.socket
%{_userunitdir}/sockets.target.wants/p11-kit-server.socket
%{_libdir}/p11-kit-proxy.so
%{_libdir}/pkcs11/*.so
%{_datadir}/bash-completion/completions/trust

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}-1
%{_libdir}/lib*%{name}.so
%{_libdir}/pkcs11/*.so
%{_libdir}/pkgconfig/%{name}-1.pc

%files trust
%{_bindir}/trust
%{_libexecdir}/p11-kit/trust-extract-compat
%{_libdir}/pkcs11/p11-kit-trust.so
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{_datadir}/bash-completion/completions/p11-kit
