#
# TODO: some unpackaged libs, should we pack them as ghosts?
#
%bcond_without	tests
Summary:	Arbitrary precision calculator
Summary(pl.UTF-8):	Kalkulator operujący na liczbach z dowolną dokładnością
Name:		calc
Version:	2.12.4.3
Release:	3
License:	LGPL v2.1+
Group:		Applications/Math
Source0:	http://www.isthe.com/chongo/src/calc/%{name}-%{version}.tar.bz2
# Source0-md5:	d95dccde71cc8d920af0f8375e85e9c8
Source1:	%{name}.desktop
Patch0:		%{name}-ppc.patch
URL:		http://www.isthe.com/chongo/tech/comp/calc/
BuildRequires:	readline-devel >= 4.2
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_check_so	1

%description
Calc is arbitrary precision arithmetic system that uses a C-like
language. Calc is useful as a calculator, an algorithm prototyped and
as a mathematical research tool. It comes with a rich set of
mathematical, programmatic and stdio functions.

%description -l pl.UTF-8
Calc jest systemem arytmetycznym o nieograniczonej dokładności,
używającym języka podobnego do C. Calc jest przydatny jako kalkulator,
narzędzie do testowania algorytmów i do badań matematycznych. Do
samego programu dołączony jest bogaty zestaw funkcji bibliotecznych -
matematycznych, programistycznych i funkcji wejścia/wyjścia

%package devel
Summary:	Calc header files and static libraries
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteki statyczne Calca
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	calc-static

%description devel
These header files and static libraries are neccessary to build
programs using Calc math libraries. These libraries contain a set of
Calc functions to use in other applications.

%description devel -l pl.UTF-8
Te pliki nagłówkowe i biblioteki statyczne są niezbędne przy budowaniu
programów wykorzystujących biblioteki matematyczne Calca. Biblioteki
te zawierające zbiór funkcji Calca do wykorzystania we własnych
programach.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 \
	LCC="%{__cc}" \
	DEBUG="%{rpmcflags}" \
	USE_READLINE=-DUSE_READLINE \
	READLINE_LIB="-lreadline -lhistory" \
	READLINE_INCLUDE=%{_includedir} \
	SCRIPTDIR=%{_datadir}/calc/cscript

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	LIBDIR=%{_libdir} \
	T=$RPM_BUILD_ROOT \
	SCRIPTDIR=%{_datadir}/calc/cscript

install -D %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

rm -f $RPM_BUILD_ROOT%{_datadir}/calc/README

find $RPM_BUILD_ROOT%{_datadir}/calc -type f | \
       xargs %{__sed} -i -e 's|#!/usr/local/bin/calc|#!%{_bindir}/calc|g'

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING is not just LGPL text, only some explanations
%doc BUGS CHANGES COPYING README
%attr(755,root,root) %{_bindir}/calc
%attr(755,root,root) %{_libdir}/libcalc.so.*.*.*.*
%attr(755,root,root) %{_libdir}/libcustcalc.so.*.*.*.*
%{_datadir}/calc
%{_desktopdir}/calc.desktop
%{_mandir}/man1/calc.1*

%files devel
%defattr(644,root,root,755)
%doc LIBRARY
%attr(755,root,root) %{_libdir}/libcalc.so
%attr(755,root,root) %{_libdir}/libcustcalc.so
%{_includedir}/calc
