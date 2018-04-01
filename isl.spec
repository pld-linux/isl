# TODO: verify gdb pretty-printers location
#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_without	static_libs	# don't build static libraries

Summary:	Library for manipulating sets and relations of integer points bounded by linear constraints
Summary(pl.UTF-8):	Biblioteka operacji na zbiorach i relacjach punktów całkowitoliczbowych z ograniczeniami liniowymi
Name:		isl
Version:	0.19
Release:	1
License:	MIT
Group:		Libraries
Source0:	http://isl.gforge.inria.fr/%{name}-%{version}.tar.xz
# Source0-md5:	1ae893020fa078531e6158cb243880a5
URL:		http://isl.gforge.inria.fr/
BuildRequires:	gmp-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with apidocs}
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	texlive-format-pdflatex
%endif
# clang can be used to generate interface/isl.py, which is not used afterwards
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API and internal documentation for isl library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki isl.

%package gdb
Summary:	GDB Python pretty printers for isl types
Summary(pl.UTF-8):	Skrypty Pythona dla GDB do ładnego wypisywania typów isl
Group:		Development/Debuggers
Requires:	gdb

%description gdb
GDB Python pretty printers for most of isl objects.

%description gdb -l pl.UTF-8
Skrypty Pythona dla GDB do ładnego wypisywania większości obiektów
isl.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/usr/%{_lib}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/libisl.so.*.*.*-gdb.py $RPM_BUILD_ROOT%{_datadir}/gdb/auto-load/usr/%{_lib}

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libisl.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog
%attr(755,root,root) %{_libdir}/libisl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libisl.so.19

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libisl.so
%{_includedir}/isl
%{_pkgconfigdir}/isl.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libisl.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/manual.pdf
%endif

%files gdb
%defattr(644,root,root,755)
%{_datadir}/gdb/auto-load/usr/%{_lib}/libisl.so.*.*.*-gdb.py
