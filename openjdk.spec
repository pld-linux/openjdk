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
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         javareldir	%{name}-%{version}
%define         javadir		%{_jvmdir}/%{javareldir}
%define         jrereldir	%{javareldir}/jre
%define         jredir		%{_jvmdir}/%{jrereldir}
%define         jvmjardir	%{_jvmjardir}/%{name}-%{version}


%define			arch		%{_arch}

%ifarch %{ix86}
%define			arch		i586
%endif

%ifarch %{x8664}
%define			arch		amd64
%endif

%define			builddir		build/%{_os}-%{arch}

# make -j1 does not work because there is some stupid magic which takes MFLAGS
# and says -jN is not allowed. remove %{_smp_mflags} from %__make.
%{expand:%%global	__make		%(echo %{__make} | sed -e 's/%{?_smp_mflags}\b//')}

%description
Open-source JDK, an implementation of the Java Platform.

%description -l pl.UTF-8:
JDK o otwartych źrodłach - implementacja platformy Java.

%package appletviewer
Summary:	Java applet viewer from openjdk
Summary(pl.UTF-8):	Przeglądarka appletów openjdk
Group:		Development/Languages/Java
Requires:	%{name} = %{version}-%{release}

%description appletviewer
This package applet viewer for openjdk.

%description appletviewer -l pl.UTF-8
Ten pakiet zawiera przeglądarkę appletów dla openjdk.

%package jre-jdbc
Summary:	JDBC files for openjdk
Summary(pl.UTF-8):	Pliki JDBC dla openjdk
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
%ifarch %{x8664}
Requires:	libodbc.so.1()(64bit)
Requires:	libodbcinst.so.1()(64bit)
%else
Requires:	libodbc.so.1
Requires:	libodbcinst.so.1
%endif
Provides:	%{name}-jdbc
Obsoletes:	java-sun-jdbc

%description jre-jdbc
This package contains JDBC files for openjdk.

%description jre-jdbc -l pl.UTF-8
Ten pakiet zawiera pliki JDBC dla openjdk.

%package jre
Summary:	Openjdk JRE (Java Runtime Environment) for Linux
Summary(pl.UTF-8):	Openjdk JRE - środowisko uruchomieniowe Javy dla Linuksa
Group:		Development/Languages/Java
Requires:	%{name}-tools = %{version}-%{release}
Requires:	jpackage-utils >= 0:1.6.6-14
Requires:	rpm-whiteout >= 1.29
Provides:	j2re = %{version}
Provides:	jaas = %{version}
Provides:	jaf = 1.1.1
Provides:	java
Provides:	java(ClassDataVersion) = %{_classdataversion}
Provides:	java1.4
Provides:	jaxp = 1.3
Provides:	jaxp_parser_impl
Provides:	jce = %{version}
Provides:	jdbc-stdext = %{version}
Provides:	jdbc-stdext = 3.0
Provides:	jmx = 1.4
Provides:	jndi = %{version}
Provides:	jndi-cos = %{version}
Provides:	jndi-dns = %{version}
Provides:	jndi-ldap = %{version}
Provides:	jndi-rmi = %{version}
Provides:	jre = %{version}
Provides:	jsse = %{version}
Provides:	xml-commons-apis
Obsoletes:	jaas
Obsoletes:	java-blackdown-jre
Obsoletes:	jaxp
Obsoletes:	jce
Obsoletes:	jdbc-stdext
Obsoletes:	jmx
Obsoletes:	jndi
Obsoletes:	jndi-provider-cosnaming
Obsoletes:	jndi-provider-dns
Obsoletes:	jndi-provider-ldap
Obsoletes:	jndi-provider-rmiregistry
Obsoletes:	jre
Obsoletes:	jsse

%description jre
Java Runtime Environment for Linux. Does not contain any X11-related
compontents.

%description jre -l pl.UTF-8
Środowisko uruchomieniowe Javy dla Linuksa. Nie zawiera żadnych
elementów związanych ze środowiskiem X11.

%package jre-X11
Summary:	Openjdk JRE (Java Runtime Environment) for Linux, X11 related parts
Summary(pl.UTF-8):	Openjdk JRE - środowisko uruchomieniowe Javy dla Linuksa, części korzystające z X11
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
# Provides:   javaws = %{version}
Provides:	jre-X11 = %{version}

%description jre-X11
X11-related part of Java Runtime Environment for Linux.

%description jre-X11 -l pl.UTF-8
Środowisko uruchomieniowe Javy dla Linuksa, część związana ze
środowiskiem graficznym X11.

%package jre-alsa
Summary:	JRE module for ALSA sound support
Summary(pl.UTF-8):	Moduł JRE do obsługi dźwięku poprzez ALSA
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
Provides:	%{name}-alsa
Obsoletes:	java-sun-alsa

%description jre-alsa
JRE module for ALSA sound support.

%description jre-alsa -l pl.UTF-8
Moduł JRE do obsługi dźwięku poprzez ALSA.

%package tools
Summary:	Shared Java tools
Summary(pl.UTF-8):	Współdzielone narzędzia Javy
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
Requires:	rpm-whiteout >= 1.29
Provides:	jar
Provides:	java-jre-tools
Provides:	java-shared
Obsoletes:	fastjar
Obsoletes:	jar
Obsoletes:	java-jre-tools
Obsoletes:	java-shared

%description tools
This package contains tools that are common for every Java(TM)
implementation, such as rmic or jar.

%description tools -l pl.UTF-8
Pakiet ten zawiera narzędzia wspólne dla każdej implementacji
Javy(TM), takie jak rmic czy jar.

%package demos
Summary:	JDK demonstration programs
Summary(pl.UTF-8):	Programy demonstracyjne do JDK
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}
Obsoletes:	java-blackdown-demos
Obsoletes:	jdk-demos

%description demos
JDK demonstration programs.

%description demos -l pl.UTF-8
Programy demonstracyjne do JDK.

%package -n browser-plugin-%{name}
Summary:	Java plugin for WWW browsers
Summary(pl.UTF-8):	Wtyczka Javy do przeglądarek WWW
Group:		Development/Languages/Java
Requires:	%{name}-jre-X11 = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Provides:	%{name}-mozilla-plugin
Provides:	mozilla-firefox-plugin-%{name}
Provides:	mozilla-plugin-%{name}
Obsoletes:	blackdown-java-sdk-mozilla-plugin
Obsoletes:	browser-plugin-openjdk-ng
Obsoletes:	java-blackdown-mozilla-plugin
Obsoletes:	jre-mozilla-plugin
Obsoletes:	mozilla-firefox-plugin-java-blackdown
Obsoletes:	mozilla-plugin-blackdown-java-sdk
Obsoletes:	mozilla-plugin-java-blackdown

%description -n browser-plugin-%{name}
Java plugin for WWW browsers.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka z obsługą Javy dla przeglądarek WWW.

%package -n browser-plugin-%{name}-ng
Summary:	Next-Generation Java plugin for WWW browsers
Summary(pl.UTF-8):	Wtyczka Javy Nowej Generacji do przeglądarek WWW
Group:		Development/Languages/Java
Requires:	%{name}-jre-X11 = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})
Provides:	%{name}-mozilla-plugin
Provides:	mozilla-firefox-plugin-%{name}
Provides:	mozilla-plugin-%{name}
Obsoletes:	blackdown-java-sdk-mozilla-plugin
Obsoletes:	browser-plugin-openjdk
Obsoletes:	java-blackdown-mozilla-plugin
Obsoletes:	jre-mozilla-plugin
Obsoletes:	mozilla-firefox-plugin-java-blackdown
Obsoletes:	mozilla-plugin-blackdown-java-sdk
Obsoletes:	mozilla-plugin-java-blackdown

%description -n browser-plugin-%{name}-ng
Next-Generation Java plugin for WWW browsers. Works only with
Firefox/Iceweasel 3.x.

%description -n browser-plugin-%{name}-ng -l pl.UTF-8
Wtyczka Nowej Generacji z obsługą Javy dla przeglądarek WWW. Działa
tylko z Firefoxem/Iceweaselem 3.x.

%package sources
Summary:	JDK sources
Summary(pl.UTF-8):	Źródła JDK
Group:		Development/Languages/Java
Requires:	%{name}-jre = %{version}-%{release}

%description sources
Sources for package JDK.

%description sources -l pl.UTF-8
Źródła dla pakietu JDK.

%prep
%setup -qc
%patch0 -p0

%build
smp_mflags=%{?_smp_mflags}
HOTSPOT_BUILD_JOBS=${smp_mflags#-j}
unset JAVA_HOME
unset CLASSPATH

export JAVA_HOME CLASSPATH HOTSPOT_BUILD_JOBS

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

install -d $RPM_BUILD_ROOT{%{jvmjardir},%{_javadir},%{_mandir}/{,ja/}man1,%{_bindir},%{_jvmdir}}

cp -a %{builddir}/j2sdk-image $RPM_BUILD_ROOT%{javadir}
rm -f $RPM_BUILD_ROOT%{javadir}/{,jre/}{ASSEMBLY_EXCEPTION,LICENSE,THIRD_PARTY_README}

cd $RPM_BUILD_ROOT%{javadir}/bin
for I in *; do
	ln -s %{javadir}/bin/$I $RPM_BUILD_ROOT%{_bindir}/$I
done
cd -

cd $RPM_BUILD_ROOT%{jredir}/bin
for I in *; do
	ln -sf %{javadir}/bin/$I $RPM_BUILD_ROOT%{jredir}/bin/$I
done
cd -

ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jsse.jar
ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jcert.jar
ln -sf %{jredir}/lib/jsse.jar $RPM_BUILD_ROOT%{jvmjardir}/jnet.jar
ln -sf %{jredir}/lib/jce.jar $RPM_BUILD_ROOT%{jvmjardir}/jce.jar
for f in jndi jndi-ldap jndi-cos jndi-rmi jaas jdbc-stdext jdbc-stdext-3.0 \
    sasl jaxp_parser_impl jaxp_transform_impl jaxp jmx activation xml-commons-apis \
    jndi-dns jndi-rmi; do
	ln -sf %{jredir}/lib/rt.jar $RPM_BUILD_ROOT%{jvmjardir}/$f.jar
done

# install -d $RPM_BUILD_ROOT%{jredir}/javaws
# cp -a jre/javaws/* $RPM_BUILD_ROOT%{jredir}/javaws
# ln -sf %{jredir}/lib/javaws.jar $RPM_BUILD_ROOT%{jvmjardir}/javaws.jar

rm -rf $RPM_BUILD_ROOT%{javadir}/man
cp -a %{builddir}/j2sdk-image/man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
cp -a %{builddir}/j2sdk-image/man/ja/man1/* $RPM_BUILD_ROOT%{_mandir}/ja/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ASSEMBLY_EXCEPTION README THIRD_PARTY_README TRADEMARK
%attr(755,root,root) %{_bindir}/appletviewer
%attr(755,root,root) %{_bindir}/apt
%attr(755,root,root) %{_bindir}/extcheck
%attr(755,root,root) %{_bindir}/idlj
%attr(755,root,root) %{_bindir}/jarsigner
%attr(755,root,root) %{_bindir}/javac
%attr(755,root,root) %{_bindir}/javadoc
%attr(755,root,root) %{_bindir}/javah
%attr(755,root,root) %{_bindir}/javap
%attr(755,root,root) %{_bindir}/jconsole
%attr(755,root,root) %{_bindir}/jdb
%attr(755,root,root) %{_bindir}/jhat
%attr(755,root,root) %{_bindir}/jinfo
%attr(755,root,root) %{_bindir}/jmap
%attr(755,root,root) %{_bindir}/jps
%attr(755,root,root) %{_bindir}/jrunscript
%attr(755,root,root) %{_bindir}/jsadebugd
%attr(755,root,root) %{_bindir}/jstack
%attr(755,root,root) %{_bindir}/jstat
%attr(755,root,root) %{_bindir}/jstatd
%attr(755,root,root) %{_bindir}/native2ascii
%attr(755,root,root) %{_bindir}/schemagen
%attr(755,root,root) %{_bindir}/serialver
%attr(755,root,root) %{_bindir}/servertool
%attr(755,root,root) %{_bindir}/wsgen
%attr(755,root,root) %{_bindir}/wsimport
%attr(755,root,root) %{_bindir}/xjc

%attr(755,root,root) %{javadir}/bin/appletviewer
%attr(755,root,root) %{javadir}/bin/apt
%attr(755,root,root) %{javadir}/bin/extcheck
%attr(755,root,root) %{javadir}/bin/idlj
%attr(755,root,root) %{javadir}/bin/jarsigner
%attr(755,root,root) %{javadir}/bin/javac
%attr(755,root,root) %{javadir}/bin/javadoc
%attr(755,root,root) %{javadir}/bin/javah
%attr(755,root,root) %{javadir}/bin/javap
%attr(755,root,root) %{javadir}/bin/jconsole
%attr(755,root,root) %{javadir}/bin/jdb
%attr(755,root,root) %{javadir}/bin/jhat
%attr(755,root,root) %{javadir}/bin/jinfo
%attr(755,root,root) %{javadir}/bin/jmap
%attr(755,root,root) %{javadir}/bin/jps
%attr(755,root,root) %{javadir}/bin/jrunscript
%attr(755,root,root) %{javadir}/bin/jsadebugd
%attr(755,root,root) %{javadir}/bin/jstack
%attr(755,root,root) %{javadir}/bin/jstat
%attr(755,root,root) %{javadir}/bin/jstatd
%attr(755,root,root) %{javadir}/bin/native2ascii
%attr(755,root,root) %{javadir}/bin/schemagen
%attr(755,root,root) %{javadir}/bin/serialver
%attr(755,root,root) %{javadir}/bin/servertool
%attr(755,root,root) %{javadir}/bin/wsgen
%attr(755,root,root) %{javadir}/bin/wsimport
%attr(755,root,root) %{javadir}/bin/xjc

%{javadir}/include
%dir %{javadir}/lib
%attr(755,root,root) %{javadir}/lib/jexec
%{javadir}/lib/ct.sym
%{javadir}/lib/*.jar
%{javadir}/lib/*.idl

%{_mandir}/man1/appletviewer.1*
%{_mandir}/man1/apt.1*
%{_mandir}/man1/extcheck.1*
%{_mandir}/man1/idlj.1*
%{_mandir}/man1/jarsigner.1*
%{_mandir}/man1/javac.1*
%{_mandir}/man1/javadoc.1*
%{_mandir}/man1/javah.1*
%{_mandir}/man1/javap.1*
%{_mandir}/man1/jconsole.1*
%{_mandir}/man1/jdb.1*
%{_mandir}/man1/jhat.1*
%{_mandir}/man1/jinfo.1*
%{_mandir}/man1/jmap.1*
%{_mandir}/man1/jps.1*
%{_mandir}/man1/jrunscript.1*
%{_mandir}/man1/jsadebugd.1*
%{_mandir}/man1/jstack.1*
%{_mandir}/man1/jstat.1*
%{_mandir}/man1/jstatd.1*
%{_mandir}/man1/native2ascii.1*
%{_mandir}/man1/schemagen.1*
%{_mandir}/man1/serialver.1*
%{_mandir}/man1/servertool.1*
%{_mandir}/man1/wsgen.1*
%{_mandir}/man1/wsimport.1*
%{_mandir}/man1/xjc.1*

%lang(ja) %{_mandir}/ja/man1/appletviewer.1*
%lang(ja) %{_mandir}/ja/man1/apt.1*
%lang(ja) %{_mandir}/ja/man1/extcheck.1*
%lang(ja) %{_mandir}/ja/man1/idlj.1*
%lang(ja) %{_mandir}/ja/man1/jarsigner.1*
%lang(ja) %{_mandir}/ja/man1/javac.1*
%lang(ja) %{_mandir}/ja/man1/javadoc.1*
%lang(ja) %{_mandir}/ja/man1/javah.1*
%lang(ja) %{_mandir}/ja/man1/javap.1*
%lang(ja) %{_mandir}/ja/man1/jconsole.1*
%lang(ja) %{_mandir}/ja/man1/jdb.1*
%lang(ja) %{_mandir}/ja/man1/jhat.1*
%lang(ja) %{_mandir}/ja/man1/jinfo.1*
%lang(ja) %{_mandir}/ja/man1/jmap.1*
%lang(ja) %{_mandir}/ja/man1/jps.1*
%lang(ja) %{_mandir}/ja/man1/jrunscript.1*
%lang(ja) %{_mandir}/ja/man1/jsadebugd.1*
%lang(ja) %{_mandir}/ja/man1/jstack.1*
%lang(ja) %{_mandir}/ja/man1/jstat.1*
%lang(ja) %{_mandir}/ja/man1/jstatd.1*
%lang(ja) %{_mandir}/ja/man1/native2ascii.1*
%lang(ja) %{_mandir}/ja/man1/schemagen.1*
%lang(ja) %{_mandir}/ja/man1/serialver.1*
%lang(ja) %{_mandir}/ja/man1/servertool.1*
%lang(ja) %{_mandir}/ja/man1/wsgen.1*
%lang(ja) %{_mandir}/ja/man1/wsimport.1*
%lang(ja) %{_mandir}/ja/man1/xjc.1*

%files jre
%defattr(644,root,root,755)
%dir %{javadir}
%dir %{javadir}/bin
%dir %{jredir}
%dir %{jredir}/bin
%attr(755,root,root) %{_bindir}/java
%attr(755,root,root) %{_bindir}/keytool
%attr(755,root,root) %{_bindir}/orbd
%attr(755,root,root) %{_bindir}/pack200
%attr(755,root,root) %{_bindir}/policytool
%attr(755,root,root) %{_bindir}/rmid
%attr(755,root,root) %{_bindir}/servertool
%attr(755,root,root) %{_bindir}/tnameserv
%attr(755,root,root) %{_bindir}/unpack200

%attr(755,root,root) %{jredir}/bin/java
%attr(755,root,root) %{jredir}/bin/keytool
%attr(755,root,root) %{jredir}/bin/orbd
%attr(755,root,root) %{jredir}/bin/pack200
%attr(755,root,root) %{jredir}/bin/policytool
%attr(755,root,root) %{jredir}/bin/rmid
%attr(755,root,root) %{jredir}/bin/servertool
%attr(755,root,root) %{jredir}/bin/tnameserv
%attr(755,root,root) %{jredir}/bin/unpack200

%attr(755,root,root) %{javadir}/bin/java
%attr(755,root,root) %{javadir}/bin/keytool
%attr(755,root,root) %{javadir}/bin/orbd
%attr(755,root,root) %{javadir}/bin/pack200
%attr(755,root,root) %{javadir}/bin/policytool
%attr(755,root,root) %{javadir}/bin/rmid
%attr(755,root,root) %{javadir}/bin/servertool
%attr(755,root,root) %{javadir}/bin/tnameserv
%attr(755,root,root) %{javadir}/bin/unpack200

%dir %{jredir}/lib
%{jredir}/lib/applet
%{jredir}/lib/cmm
%{jredir}/lib/ext

%dir %{jredir}/lib/%{arch}
%dir %{jredir}/lib/%{arch}/headless
%dir %{jredir}/lib/%{arch}/jli
%attr(755,root,root) %{jredir}/lib/%{arch}/native_threads
%attr(755,root,root) %{jredir}/lib/%{arch}/server
%attr(755,root,root) %{jredir}/lib/%{arch}/jli/libjli.so
%{jredir}/lib/%{arch}/jvm.cfg
%attr(755,root,root) %{jredir}/lib/%{arch}/lib[acdfhijmnrvz]*.so
%exclude %{jredir}/lib/%{arch}/libjsoundalsa.so
%ifarch %{ix86}
%attr(755,root,root) %{jredir}/lib/%{arch}/client
%endif
%attr(755,root,root) %{jredir}/lib/%{arch}/libsplashscreen.so

%{jredir}/lib/im
%{jredir}/lib/images
%attr(755,root,root) %{jredir}/lib/jexec
%{jredir}/lib/meta-index
%dir %{jredir}/lib/security
%{jredir}/lib/security/*.*
%verify(not md5 mtime size) %config(noreplace) %{jredir}/lib/security/cacerts
%{jredir}/lib/zi
%{jredir}/lib/*.jar
%{jredir}/lib/*.properties
%lang(ja) %{jredir}/lib/*.properties.ja
%dir %{jvmjardir}
%{jvmjardir}/activation.jar
%{jvmjardir}/jaas.jar
%{jvmjardir}/jce.jar
%{jvmjardir}/jcert.jar
%{jvmjardir}/jdbc-stdext*.jar
%{jvmjardir}/jmx.jar
%{jvmjardir}/jndi*.jar
%{jvmjardir}/jnet.jar
%{jvmjardir}/jsse.jar
%{jvmjardir}/sasl.jar
%{jvmjardir}/jaxp*.jar
%{jvmjardir}/xml-commons*.jar
%{jredir}/lib/classlist
%{jredir}/lib/fontconfig.bfc
%{jredir}/lib/fontconfig.Fedora.bfc
%{jredir}/lib/fontconfig.Fedora.properties.src
%{jredir}/lib/fontconfig.properties.src
%{jredir}/lib/fontconfig.SuSE.bfc
%{jredir}/lib/fontconfig.SuSE.properties.src
%{jredir}/lib/fontconfig.Ubuntu.bfc
%{jredir}/lib/fontconfig.Ubuntu.properties.src
%attr(755,root,root) %{jredir}/lib/%{arch}/headless/libmawt.so
%attr(755,root,root) %{jredir}/lib/%{arch}/libsaproc.so
%attr(755,root,root) %{jredir}/lib/%{arch}/libunpack.so
%dir %{jredir}/lib/management
%{jredir}/lib/management/jmxremote.access
%{jredir}/lib/management/jmxremote.password.template
%{jredir}/lib/management/management.properties
%{jredir}/lib/management/snmp.acl.template

%{_mandir}/man1/java.1*
%{_mandir}/man1/keytool.1*
%{_mandir}/man1/orbd.1*
%{_mandir}/man1/pack200.1*
%{_mandir}/man1/policytool.1*
%{_mandir}/man1/rmid.1*
%{_mandir}/man1/servertool.1*
%{_mandir}/man1/tnameserv.1*
%{_mandir}/man1/unpack200.1*

%lang(ja) %{_mandir}/ja/man1/java.1*
%lang(ja) %{_mandir}/ja/man1/keytool.1*
%lang(ja) %{_mandir}/ja/man1/orbd.1*
%lang(ja) %{_mandir}/ja/man1/pack200.1*
%lang(ja) %{_mandir}/ja/man1/policytool.1*
%lang(ja) %{_mandir}/ja/man1/rmid.1*
%lang(ja) %{_mandir}/ja/man1/servertool.1*
%lang(ja) %{_mandir}/ja/man1/tnameserv.1*
%lang(ja) %{_mandir}/ja/man1/unpack200.1*

%files jre-alsa
%defattr(644,root,root,755)
%attr(755,root,root) %{jredir}/lib/%{arch}/libjsoundalsa.so

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/jar
%attr(755,root,root) %{_bindir}/rmic
%attr(755,root,root) %{_bindir}/rmiregistry
%attr(755,root,root) %{jredir}/bin/rmiregistry
%attr(755,root,root) %{javadir}/bin/jar
%attr(755,root,root) %{javadir}/bin/rmic
%attr(755,root,root) %{javadir}/bin/rmiregistry
%{_mandir}/man1/jar.1*
%{_mandir}/man1/rmic.1*
%{_mandir}/man1/rmiregistry.1*
%lang(ja) %{_mandir}/ja/man1/jar.1*
%lang(ja) %{_mandir}/ja/man1/rmic.1*
%lang(ja) %{_mandir}/ja/man1/rmiregistry.1*

%files demos
%defattr(644,root,root,755)
%dir %{javadir}/demo
%{javadir}/demo/applets
%{javadir}/demo/jfc
%{javadir}/demo/jpda
%dir %{javadir}/demo/jvmti
%dir %{javadir}/demo/jvmti/[!i]*
%dir %{javadir}/demo/jvmti/*/lib
%attr(755,root,root) %{javadir}/demo/jvmti/*/lib/*.so
%{javadir}/demo/jvmti/*/src.zip
%{javadir}/demo/jvmti/*/README.txt
%{javadir}/demo/jvmti/*/*.jar
%{javadir}/demo/management
%{javadir}/demo/nbproject
%{javadir}/demo/scripting
%{javadir}/sample
