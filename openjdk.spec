# TODO
# - all

# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 50.0
Summary:	Open-source JDK, an implementation of the Java Platform
Summary(pl.UTF-8):	JDK o otwartych źrodłach - implementacja platformy Java
Name:		openjdk
Version:	1.7.0
Release:	0.1
License:	GPL v2
Group:		Development/Languages/Java
Source0:	http://www.java.net/download/openjdk/jdk7/promoted/b10/compiler-7-ea-src-b10-21_mar_2007.zip
# Source0-md5:	a7be9da818adff098c00b00a983b0e40
Source1:	http://www.java.net/download/openjdk/jdk7/promoted/b10/hotspot-7-ea-src-b10-21_mar_2007.zip
# Source1-md5:	df51d7e061c3e97adf7a61a406c42d74
Source2:	http://www.java.net/download/openjdk/jdk7/promoted/b10/jtreg_bin-3_2_2_01-fcs-bin-b03-21_Mar_2007.zip
# Source2-md5:	1b501642684b7cfe8aff3fa60c5a2083
Source3:	Test.java
URL:		https://openjdk.dev.java.net/
BuildRequires:	ant
BuildRequires:	file
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	libstdc++-devel
BuildRequires:	rpmbuild(macros) >= 1.357
Provides:	java(ClassDataVersion) = %{_classdataversion}
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Today this project contains two significant components of the JDK:
- The HotSpot Virtual Machine
- The Java programming-language compiler (javac), with complete
  NetBeans project metadata

%description -l pl.UTF-8:
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
%{__make} \
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
install -d $RPM_BUILD_ROOT{%{_javadir},%{_bindir}}
cp -a compiler/dist/lib/javac.jar $RPM_BUILD_ROOT%{_javadir}/javac-%{version}.jar
ln -s javac-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/javac.jar
install javac $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc compiler/doc/*
%attr(755,root,root) %{_bindir}/javac
%{_javadir}/javac-%{version}.jar
%{_javadir}/javac.jar
