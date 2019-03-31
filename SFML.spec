#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	SFML - Simple and Fast Multimedia Library
Summary(pl.UTF-8):	SFML - prosta i szybka biblioteka multimedialna
Name:		SFML
Version:	2.1
Release:	6
License:	BSD-like
Group:		Libraries
Source0:	http://sfml-dev.org/download/sfml/2.1/%{name}-%{version}-sources.zip
# Source0-md5:	2de81448733f3f46964f23f41cd42e92
Patch0:		%{name}-glx.patch
URL:		http://sfml-dev.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	cmake >= 2.8
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	freetype-devel >= 2
BuildRequires:	glew-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libstdc++-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SFML is a simple, fast, cross-platform and object-oriented multimedia
API. It provides access to windowing, graphics, audio and network. It
is written in C++, and has bindings for various languages such as C,
.NET, Ruby, Python.

%description -l pl.UTF-8
SFML to prosta, szybka, wieloplatformowa biblioteka multimedialna z
API zorientowanym obiektowo. Zapewnia dostęp do okienek, grafiki,
dźwięku i sieci. Jest napisana w C++ i ma dowiązania do różnych innych
języków, takich jak C, .NET, Ruby, Python.

%package devel
Summary:	Header files for SFML library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki SFML
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-devel
Requires:	libstdc++-devel

%description devel
Header files for SFML library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki SFML.

%package apidocs
Summary:	SFML API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki SFML
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for SFML library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki SFML.

%prep
%setup -q
%patch0 -p1

# use system files
%{__rm} -r src/SFML/Window/glext

%build
%cmake . \
	%{?with_apidocs:-DSFML_BUILD_DOC=ON}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_datadir}/SFML/*.txt
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/SFML/doc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc license.txt readme.txt
%attr(755,root,root) %{_libdir}/libsfml-audio.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsfml-audio.so.2
%attr(755,root,root) %{_libdir}/libsfml-graphics.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsfml-graphics.so.2
%attr(755,root,root) %{_libdir}/libsfml-network.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsfml-network.so.2
%attr(755,root,root) %{_libdir}/libsfml-system.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsfml-system.so.2
%attr(755,root,root) %{_libdir}/libsfml-window.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libsfml-window.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libsfml-audio.so
%attr(755,root,root) %{_libdir}/libsfml-graphics.so
%attr(755,root,root) %{_libdir}/libsfml-network.so
%attr(755,root,root) %{_libdir}/libsfml-system.so
%attr(755,root,root) %{_libdir}/libsfml-window.so
%{_includedir}/SFML
%{_pkgconfigdir}/sfml-all.pc
%{_pkgconfigdir}/sfml-audio.pc
%{_pkgconfigdir}/sfml-graphics.pc
%{_pkgconfigdir}/sfml-network.pc
%{_pkgconfigdir}/sfml-system.pc
%{_pkgconfigdir}/sfml-window.pc
%dir %{_datadir}/SFML
%{_datadir}/SFML/cmake

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
