# TODO: install gdb pretty-printer properly (see files)
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries
%bcond_without	piplib		# PipLib solver (stubs are used instead)
#
Summary:	Library for manipulating sets and relations of integer points bounded by linear constraints
Summary(pl.UTF-8):	Biblioteka operacji na zbiorach i relacjach punktów całkowitoliczbowych z ograniczeniami liniowymi
Name:		isl
Version:	0.09
Release:	1
License:	LGPL v2.1
Group:		Libraries
Source0:	ftp://ftp.linux.student.kuleuven.be/pub/people/skimo/isl/%{name}-%{version}.tar.lzma
# Source0-md5:	d6ccfc11197c958c4e7f16937ca56004
URL:		http://freecode.com/projects/isl
BuildRequires:	gmp-devel
%{?with_piplib:BuildRequires:	piplib-devel >= 1.3.6}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	texlive-format-pdflatex
%endif
%{?with_piplib:Requires:	piplib >= 1.3.6}
# clang?
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
isl is a library for manipulating sets and relations of integer points
bounded by linear constraints. Supported operations on sets include
intersection, union, set difference, emptiness check, convex hull,
(integer) affine hull, integer projection, and computing the
lexicographic minimum using parametric integer programming. It also
includes an ILP solver based on generalized basis reduction.

%description -l pl.UTF-8
isl to biblioteka do operacji na zbiorach i relacjach punktów
całkowitoliczbowych z ograniczeniami liniowymi. Obsługiwane operacje
na zbiorach obejmują przecięcia, sumy, różnice, sprawdzanie, czy zbiór
jest pusty, wyznaczanie powłoki wypukłej, wyznaczanie
(całkowitoliczbowej) powłoki afinicznej, rzuty całkowitoliczbowe oraz
obliczanie minimum leksykograficznego przy użyciu parametrycznego
programowania liniowego. Biblioteka obsługuje także rozwiazywanie
całkowitoliczbowych problemów liniowych w oparciu o redukcję bazy.

%package devel
Summary:	Header files for isl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki isl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gmp-devel
%{?with_piplib:Requires:	piplib-devel >= 1.3.6}

%description devel
Header files for isl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki isl.

%package static
Summary:	Static isl library
Summary(pl.UTF-8):	Statyczna biblioteka isl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static isl library.

%description static -l pl.UTF-8
Statyczna biblioteka isl.

%package apidocs
Summary:	isl API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki isl
Group:		Documentation

%description apidocs
API and internal documentation for isl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki isl.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{?with_piplib:--with-piplib=system}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_libdir}/libisl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libisl.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libisl.so
%{_libdir}/libisl.la
%{_includedir}/isl
%{_pkgconfigdir}/isl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libisl.a

# TODO: package gdb pretty printer properly
#%{_libdir}/libisl.so.*.*.*-gdb.py

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/manual.pdf
%endif
