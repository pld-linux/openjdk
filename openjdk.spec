#
# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion	50.0
%define		buildnum		b17

# It does not work with openjdk Makefile. Use HOTSPOT_BUILD_JOBS instead.
%undefine	_smp_mflags

Summary:	Open-source JDK, an implementation of the Java Platform
Summary(pl.UTF-8):	JDK o otwartych źrodłach - implementacja platformy Java
Name:		openjdk
Version:	1.6.%{buildnum}
Release:	0.1
License:	GPL v2
Group:		Applications
Source0:	http://download.java.net/openjdk/jdk6/promoted/%{buildnum}/%{name}-6-src-%{buildnum}-14_oct_2009.tar.gz
# Source0-md5:	078fe0ab744c98694decc77f2456c560
Patch0:		%{name}-build.patch
URL:		http://openjdk.dev.java.net/
BuildRequires:	ant
BuildRequires:	cups-devel
BuildRequires:	file
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	libstdc++-devel
BuildRequires:	libstdc++-static
BuildRequires:	rpmbuild(macros) >= 1.357
Provides:	java(ClassDataVersion) = %{_classdataversion}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Open-source JDK, an implementation of the Java Platform.

%description -l pl.UTF-8:
JDK o otwartych źrodłach - implementacja platformy Java.

%prep
%setup -q -c

%patch0 -p0

%build
unset JAVA_HOME
unset CLASSPATH
LC_ALL=C
LANG=C
HOTSPOT_BUILD_JOBS=%(_NCPUS=$(/usr/bin/getconf _NPROCESSORS_ONLN); [ "$_NCPUS" -gt 1 ] && echo "$(($_NCPUS * 2))")
export JAVA_HOME CLASSPATH LC_ALL LANG HOTSPOT_BUILD_JOBS

/usr/bin/make sanity
/usr/bin/make \
	UTILS_USR_BIN_PATH="" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_CFLAGS="%{rpmcflags}" \
	WARNINGS_ARE_ERRORS='' \
	ALT_BOOTDIR=%{java_home} \
%ifarch %{x8664}
	ARCH_DATA_MODEL=64
%endif

%install
rm -rf $RPM_BUILD_ROOT

/usr/bin/make export_product \
	ALT_BOOTDIR=%{java_home} \
	EXPORT_PATH=$RPM_BUILD_ROOT%{_prefix} \
	EXPORT_LIB_DIR=$RPM_BUILD_ROOT%{_libdir} \
	EXPORT_JRE_LIB_ARCH_DIR=$RPM_BUILD_ROOT%{_libdir}/jre \
	EXPORT_DOCS_DIR=$RPM_BUILD_ROOT%{_docdir} \
%ifarch %{x8664}
	ARCH_DATA_MODEL=64
%endif

rm -rf jvmti
mv $RPM_BUILD_ROOT%{_docdir}/platform/jvmti .

install -d $RPM_BUILD_ROOT{%{_javadir},%{_bindir}}
cp -a compiler/dist/lib/javac.jar $RPM_BUILD_ROOT%{_javadir}/javac-%{version}.jar
ln -s javac-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/javac.jar
install javac $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS CREDITS ChangeLog NEWS README THANKS TODO
