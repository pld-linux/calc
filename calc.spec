Summary:	Arbitrary precision calculator
Summary(pl.UTF-8):	Kalkulator operujący na liczbach z dowolną dokładnością
Name:		calc
Version:	2.12.1.11
Release:	1
License:	LGPL
Group:		Applications/Math
Source0:	http://www.isthe.com/chongo/src/calc/%{name}-%{version}.tar.gz
# Source0-md5:	515ee5bbe7ec3e335048052c84885ed7
Source1:	%{name}.desktop
URL:		http://www.isthe.com/chongo/tech/comp/calc/
BuildRequires:	sed >= 4.0
BuildRequires:	readline-devel >= 4.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
# only static libraries now
# to be changed after switching to shared lib
#Requires:	%{name} = %{version}
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

%build
%{__make} -j1 \
	LCC="%{__cc}" \
	DEBUG="%{rpmcflags}" \
	USE_READLINE=-DUSE_READLINE \
	READLINE_LIB="-lreadline -lhistory" \
	READLINE_INCLUDE=%{_includedir} \
	SCRIPTDIR=%{_datadir}/calc/cscript

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/calc/{cscript,custom,help} \
	$RPM_BUILD_ROOT{%{_includedir},%{_mandir}/man1,%{_libdir}} \
	$RPM_BUILD_ROOT{%{_bindir},%{_desktopdir}}

%{__make} install \
	T=$RPM_BUILD_ROOT \
	SCRIPTDIR=%{_datadir}/calc/cscript

mv -f $RPM_BUILD_ROOT%{_datadir}/calc/custom/libcustcalc.a $RPM_BUILD_ROOT%{_libdir}
mv -f cal/README README.cal

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop

rm -f $RPM_BUILD_ROOT%{_datadir}/calc/README

find $RPM_BUILD_ROOT%{_datadir}/calc -type f | \
       xargs %{__sed} -i -e 's|#!/usr/local/bin/calc|#!%{_bindir}/calc|g'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# COPYING is not just LGPL text, only some explanations
%doc BUGS CHANGES COPYING README
%attr(755,root,root) %{_bindir}/*
%{_datadir}/calc
%{_mandir}/man*/*
%{_desktopdir}/*.desktop

%files devel
%defattr(644,root,root,755)
%doc LIBRARY sample/README_SAMPLE
%{_libdir}/lib*.a
%{_includedir}/calc
