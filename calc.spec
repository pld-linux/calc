Summary:	Arbitrary precision calculator
Summary(pl):	Kalkulator operuj±cy na liczbach z dowoln± dok³adno¶ci±
Name:		calc
Version:	2.11.2t1.0
Release:	1
License:	GPL
Group:		Applications/Math
Group(pl):	Aplikacje/Matematyczne
Source0:	ftp://ftp.uu.net/pub/calc/%{name}-%{version}.tar.gz
BuildRequires:	readline-devel >= 4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Calc is arbitrary precision arithmetic system that uses a C-like
language. Calc is useful as a calculator, an algorithm prototyped and
as a mathematical research tool. It comes with a rich set of
mathematical, programmatic and stdio functions.

%description -l pl
Calc jest systemem arytmetycznym o nieograniczonej dok³adno¶ci,
u¿ywaj±cym jêzyka podobnego do C. Calc jest przydatny jako kalkulator,
narzêdzie do testowania algorytmów i do badañ matematycznych. Do
samego programu do³±czony jest bogaty zestaw funkcji bibliotecznych -
matematycznych, programistycznych i funkcji wej¶cia/wyj¶cia

%package devel
Summary:	Calc header files
Summary(pl):	Pliki nag³ówkowe Calca
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	calc = %{version}

%description devel
These header files are neccessary to build programs using Calc math
libraries.

%description devel -l pl
Te pliki nag³ówkowe s± niezbêdne przy budowaniu programów
wykorzystuj±cych biblioteki matematyczne Calca.

%package static
Summary:	Calc static libraries
Summary(pl):	Biblioteki statyczne Calca
Group:		Development/Libraries
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Requires:	%{name}-devel = %{version}

%description static
Libraries containing a set of Calc functions to use in other
applications.

%description static -l pl
Biblioteki zawieraj±ce komplet funkcji Calca do wykorzystania we
w³asnych programach.

%prep
%setup  -q

%build
%{__make} CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
	USE_READLINE=-DUSE_READLINE \
	READLINE_LIB="-lreadline -lhistory" \
	READLINE_INCLUDE=%{_includedir} \
	BINDIR=%{_bindir} \
	TOPDIR=%{_datadir} \
	INCDIR=%{_includedir} \
	MANDIR=%{_mandir}/man1 \
	HELPDIR=%{_datadir}/calc/help \
	CUSTOMLIBDIR=%{_datadir}/calc/custom \
	CUSTOMHELPDIR=%{_datadir}/calc/custhelp \
	SCRIPTDIR=%{_datadir}/calc/cscript

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/calc/{cscript,custom,help} \
	$RPM_BUILD_ROOT{%{_includedir},%{_mandir}/man1,%{_libdir}} \
	$RPM_BUILD_ROOT%{_bindir}

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	TOPDIR=$RPM_BUILD_ROOT%{_datadir} \
	INCDIR=$RPM_BUILD_ROOT%{_includedir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
	HELPDIR=$RPM_BUILD_ROOT%{_datadir}/calc/help \
	CUSTOMLIBDIR=$RPM_BUILD_ROOT%{_datadir}/calc/custom \
	CUSTOMHELPDIR=$RPM_BUILD_ROOT%{_datadir}/calc/custhelp \
	SCRIPTDIR=$RPM_BUILD_ROOT%{_datadir}/calc/cscript

mv -f $RPM_BUILD_ROOT%{_datadir}/calc{/,/custom}/*.a $RPM_BUILD_ROOT%{_libdir}
mv -f cal/README README-cal

rm -f $RPM_BUILD_ROOT%{_datadir}/calc/README

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	BUGS CHANGES README README-cal LIBRARY sample/README_SAMPLE

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz 
%attr(755,root,root) %{_bindir}/*
%{_datadir}/calc
%{_mandir}/man*/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%doc sample/*

%files static
%defattr(644,root,root,755)
%{_libdir}/*
