#
# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion	50.0
%define		buildnum		17

Summary:	Open-source JDK, an implementation of the Java Platform
Summary(pl.UTF-8):	JDK o otwartych źrodłach - implementacja platformy Java
Name:		openjdk
Version:	1.6.0.%{buildnum}
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://download.java.net/openjdk/jdk6/promoted/b%{buildnum}/%{name}-6-src-b%{buildnum}-14_oct_2009.tar.gz
# Source0-md5:	078fe0ab744c98694decc77f2456c560
Patch0:		%{name}-build.patch
URL:		http://openjdk.dev.java.net/
BuildRequires:	alsa-lib-devel
BuildRequires:	ant
BuildRequires:	cups-devel
BuildRequires:	file
BuildRequires:	gawk
BuildRequires:	java-xerces
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	libstdc++-devel
BuildRequires:	libstdc++-static
BuildRequires:	openmotif-devel
BuildRequires:	procps
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	unzip
BuildRequires:	zip
Provides:	java(ClassDataVersion) = %{_classdataversion}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         javareldir	%{name}-%{version}
%define         javadir		%{_jvmdir}/%{javareldir}
%define         jrereldir	%{javareldir}/jre
%define         jredir		%{_jvmdir}/%{jrereldir}
%define         jvmjardir	%{_jvmjardir}/%{name}-%{version}


%ifarch %{ix86}
%define			arch		i586
%endif

%ifarch %{x8664}
%define			arch		amd64
%endif

%define			builddir		build/%{_os}-%{javaarch}

# make -j1 does not work because there is some stupid magick which takes MFLAGS
# and says -jN is not allowed. remove %{_smp_mflags} from %__make.
%{expand:%%global	__make		%(echo %{__make} | sed -e 's/%{?_smp_mflags}\b//')}

%description
Open-source JDK, an implementation of the Java Platform.

%description -l pl.UTF-8:
JDK o otwartych źrodłach - implementacja platformy Java.

%prep
%setup -qc
%patch0 -p0

%build
smp_mflags=%{?_smp_mflags}
HOTSPOT_BUILD_JOBS=${smp_mflags#-j}
unset JAVA_HOME
unset CLASSPATH
LC_ALL=C
LANG=C

export JAVA_HOME CLASSPATH LC_ALL LANG HOTSPOT_BUILD_JOBS

echo "Make: %{__make}"
echo "Build Jobs: $HOTSPOT_BUILD_JOBS"

%{__make} sanity
%{__make} \
	UTILS_USR_BIN_PATH="" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_CFLAGS="%{rpmcflags}" \
	WARNINGS_ARE_ERRORS='' \
	ALT_BOOTDIR=%{java_home} \

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_javadir},%{_mandir},%{_bindir},%{_jvmdir}}

cp -a %{builddir}/j2sdk-image $RPM_BUILD_ROOT%{javadir}
rm $RPM_BUILD_ROOT%{javadir}/{,jre/}{ASSEMBLY_EXCEPTION,LICENSE,THIRD_PARTY_README}

cd $RPM_BUILD_ROOT%{javadir}/bin
for I in *; do
  ln -s %{javadir}/bin/$I %{_bindir}/$I
done
cd -

cd $RPM_BUILD_ROOT%{javadir}/jre/bin
for I in *; do
  ln -s %{javadir}/jre/bin/$I %{_bindir}/$I
done
cd -

rm -rf  $RPM_BUILD_ROOT%{javadir}/man
install %{builddir}/j2sdk/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install %{builddir}/j2sdk/man/ja/man1/* $RPM_BUILD_ROOT%{_mandir}/ja/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ASSEMBLY_EXCEPTION README THIRD_PARTY_README TRADEMARK
%{_mandir}/man1/*
%lang(ja) %{_mandir}/ja/man1/*
