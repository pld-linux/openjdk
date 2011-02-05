# TODO
# - all

# broken
%define	_enable_debug_packages 0

# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 50.0
Summary:	Open-source JDK, an implementation of the Java Platform
Summary(pl.UTF-8):	JDK o otwartych źrodłach - implementacja platformy Java
Name:		openjdk
Version:	1.7.0
Release:	0.1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	http://www.java.net/download/openjdk/jdk7/promoted/b11/compiler-7-ea-src-b11-10_apr_2007.zip
# Source0-md5:	07d66408d68b41a7884cd2f176c41ce2
Source1:	http://www.java.net/download/openjdk/jdk7/promoted/b11/hotspot-7-ea-src-b11-10_apr_2007.zip
# Source1-md5:	55c9920bc0ce1b6459f09eb030b4d9d3
Source2:	http://www.java.net/download/openjdk/jdk7/promoted/b11/jtreg_bin-3_2_2_01-fcs-bin-b03-10_Apr_2007.zip
# Source2-md5:	185807a77cd29792f58291f42f6b25ac
Source3:	Test.java
URL:		https://openjdk.dev.java.net/
BuildRequires:	ant
BuildRequires:	file
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.357
BuildRequires:	unzip
Provides:	java(ClassDataVersion) = %{_classdataversion}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Today this project contains two significant components of the JDK:
- The HotSpot Virtual Machine
- The Java programming-language compiler (javac), with complete
  NetBeans project metadata

%description -l pl.UTF-8
Aktualnie ten projekt zawiera dwa znaczące składniki JDK:
- maszynę wirtualną HotSpot
- kompilator Javy (javac) z pełnymi metadanymi projektu NetBeans

%prep
%setup -qc -a1 -a2
cat <<'EOF' > javac
#!/bin/sh
exec java -jar %{_javadir}/javac-%{version}.jar ${1:+"$@"}
EOF

cp %{SOURCE3} Test.java

%build
# HotSpot
HOTSPOT_BUILD_JOBS="%(echo "%{__make}" | sed -e 's#.*-j\([[:space:]]*[0-9]\+\)#\1#g')"
[ "$HOTSPOT_BUILD_JOBS" = "%{__make}" ] && HOTSPOT_BUILD_JOBS=1
HOTSPOT_BUILD_JOBS=$(echo $HOTSPOT_BUILD_JOBS)

%{__make} \
	-j1 HOTSPOT_BUILD_JOBS=$HOTSPOT_BUILD_JOBS \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	OPT_CFLAGS="%{rpmcflags}" \
	WARNINGS_ARE_ERRORS='' \
	-C hotspot/make \
	ALT_BOOTDIR=%{java_home} \
%ifarch %{x8664}
	ARCH_DATA_MODEL=64
%endif

# Compiler
cd compiler
%ant
cd -

# Test Class Data Version
./compiler/dist/bin/javac Test.java
classver=$(file Test.class | grep -o 'compiled Java class data, version [0-9.]*' | awk '{print $NF}')
if [ "$classver" != %{_classdataversion} ]; then
	echo "Set %%define _classdataversion to $classver and rerun."
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
%{__make} export_product \
	-C hotspot/make \
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

%files
%defattr(644,root,root,755)
%doc compiler/doc/* jvmti

# hotspot
%dir %{_libdir}/jre
%attr(755,root,root) %{_libdir}/jre/libsaproc.so
%dir %{_libdir}/jre/server
%{_libdir}/jre/server/Xusage.txt
%attr(755,root,root) %{_libdir}/jre/server/libjsig.so
%attr(755,root,root) %{_libdir}/jre/server/libjvm.so
%{_libdir}/sa-jdi.jar
%{_includedir}/jmm.h
%{_includedir}/jni.h
%{_includedir}/jvmti.h
%{_includedir}/linux/jni_md.h

# compiler
%attr(755,root,root) %{_bindir}/javac
%{_javadir}/javac-%{version}.jar
%{_javadir}/javac.jar
