%define	pkgname	mozjs
%define	api	17.0
%define libname	%mklibname %{pkgname} %{api}
%define libdev %mklibname %{pkgname} %{api} -d

Summary:	JavaScript interpreter and libraries
Name:		mozjs17
Version:	17.0.0
Release:	2
License:	GPLv2+ or LGPLv2+ or MPLv1.1
Group:		Development/Other
URL:		http://www.mozilla.org/js/
Source0:	http://ftp.mozilla.org/pub/mozilla.org/js/mozjs%{version}.tar.gz
# From fedora
Patch0:		js17-build-fixes.patch
BuildRequires:	pkgconfig(nspr)
BuildRequires:	pkgconfig(python3)
BuildRequires:	readline-devel
BuildRequires:	autoconf2.1

%description
JavaScript is the Netscape-developed object scripting language used in millions
of web pages and server applications worldwide. Netscape's JavaScript is a
superset of the ECMA-262 Edition 3 (ECMAScript) standard scripting language,
with only mild differences from the published standard.

%package -n %{libname}
Summary:	JavaScript engine library
Group:		System/Libraries
Obsoletes:	%{_lib}mozjs-17 < 17.0.0-1

%description -n %{libname}
JavaScript is the Netscape-developed object scripting languages. This
package has been created for purposes of Sablotron and is suitable for
embedding in applications. See http://www.mozilla.org/js for details
and sources.

%package -n %{libdev}
Summary:	The header files for %{name}
Group:		Development/Other
Provides:	%{name}-devel = %{version}-%{release}
# Necessary because mozjs uses a weird versioning scheme instead of
# proper sonames
%if "%{_lib}" == "lib64"
Provides:	devel(libmozjs-17.0(64bit))
%else
Provides:	devel(libmozjs-17.0)
%endif
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{_lib}mozjs-17-devel < 17.0.0-1

%description -n %{libdev}
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%setup -q -n mozjs%{version}
%apply_patches

# Delete bundled sources
rm -rf js/src/editline
rm -rf js/src/ctypes/libffi

chmod a+x configure

pushd js/src
	autoconf-2.13
popd

%build
%configure2_5x --disable-static --with-system-nspr --enable-threadsafe --enable-readline
%make

%check
cat > js/src/config/find_vanilla_new_calls << EOF
#!/bin/bash
exit 0
EOF

#%make -C js/src check

%install
%makeinstall_std

# For some reason the headers and pkg-config file are executable
find %{buildroot}%{_includedir} -type f -exec chmod a-x {} \;
chmod a-x  %{buildroot}%{_libdir}/pkgconfig/*.pc

# Upstream does not honor --disable-static yet
rm -f %{buildroot}%{_libdir}/*.a

# This is also statically linked; once that is fixed that we could
# consider shipping it.
rm -f %{buildroot}%{_bindir}/js17

# However, delete js-config since everything should use
# the pkg-config file.
rm -f %{buildroot}%{_bindir}/js17-config

%files -n %{libname}
%doc LICENSE README
%{_libdir}/*.so

%files -n %{libdev}
%{_libdir}/pkgconfig/*.pc
%{_includedir}/js-17.0
