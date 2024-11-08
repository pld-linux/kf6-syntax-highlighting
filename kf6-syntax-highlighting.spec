#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.8
%define		qtver		5.15.2
%define		kfname		syntax-highlighting

Summary:	Syntax highlighting
Name:		kf6-%{kfname}
Version:	6.8.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	2e955fd3f615b550fccb3c6cace0c8f7
URL:		http://www.kde.org/
BuildRequires:	cmake >= 3.16
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
Syntax highlighting.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang syntaxhighlighting6 --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f syntaxhighlighting6.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ksyntaxhighlighter6
%ghost %{_libdir}/libKF6SyntaxHighlighting.so.6
%attr(755,root,root) %{_libdir}/libKF6SyntaxHighlighting.so.*.*
%{_datadir}/qlogging-categories6/ksyntaxhighlighting.categories
%{_datadir}/qlogging-categories6/ksyntaxhighlighting.renamecategories
%dir %{_libdir}/qt6/qml/org/kde/syntaxhighlighting
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/syntaxhighlighting/libkquicksyntaxhighlightingplugin.so
%{_libdir}/qt6/qml/org/kde/syntaxhighlighting/qmldir
%{_libdir}/qt6/qml/org/kde/syntaxhighlighting/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/syntaxhighlighting/kquicksyntaxhighlightingplugin.qmltypes

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KSyntaxHighlighting
%{_libdir}/cmake/KF6SyntaxHighlighting
%{_libdir}/libKF6SyntaxHighlighting.so
