%global gb3_ver %(rpm -q --qf '%%{version}' gambas-devel)

Summary:	A frontend for DNF
Name:		OM-dnfdrake
Version:	5.0.125
Release:	1
License:	GPLv3
Group:		Graphical desktop/KDE
URL:		https://mib.pianetalinux.org
#URL:		https://github.com/astrgl/dnfdrake
#Source0:	https://github.com/astrgl/dnfdrake/archive/%{version}/%{name}-%{version}.tar.gz
#Source:	%{name}-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz

BuildRequires:	gambas-devel
BuildRequires:	gambas-gb.dbus
BuildRequires:	gambas-gb.form
BuildRequires:	gambas-gb.form.stock
BuildRequires:	gambas-gb.qt6
BuildRequires:	gambas-gb.image
BuildRequires:	gambas-gui-backend
BuildRequires:	imagemagick

Requires:	sudo
Requires:	createrepo_c
Requires:	dnf-utils
Requires:	gambas-runtime = %{gb3_ver}
Requires:	gambas-gb.dbus = %{gb3_ver}
Requires:	gambas-gb.form = %{gb3_ver}
Requires:	gambas-gb.form.stock = %{gb3_ver}
Requires:	gambas-gb.qt6 = %{gb3_ver}
Requires:	gambas-gui-backend = %{gb3_ver}
Requires:	gambas-gb.image = %{gb3_ver}
Requires:	gambas-gb.complex = %{gb3_ver}
Requires:	lsb-release
Requires:	python-dnf-plugin-versionlock
Requires:	xrandr
#Requires:	OM-draketray

BuildArch: noarch

%description
DnfDrake is a frontend for DNF package manager
Powerful like a terminal and simple like a GUI!


%files
%license FILE-EXTRA/license
%{_bindir}/dnfdrake.gambas
%{_bindir}/dnfdrake
%dir %{_datadir}/dnfdrake
%{_datadir}/dnfdrake/*
%{_datadir}/applications/dnfdrake.desktop
%{_datadir}/pixmaps/dnfdrake.xpm
%{_iconsdir}/hicolor/*/apps/dnfdrake.png
%{_iconsdir}/hicolor/*/apps/dnfdrake.svg
%{_datadir}//polkit-1/actions/org.freedesktop.policykit.dnfdrake.policy

#---------------------------------------------------------------------------

%prep
%autosetup -p1

%build
gbc3 -e -a -g -t -f public-module -f public-control -j%{?_smp_mflags}
gba3

# unversion binary
mv %{name}-%{version}.gambas dnfdrake.gambas

%install
# binary - OK
install -Dm 0755 dnfdrake.gambas -t %{buildroot}/%{_bindir}/
install -Dm 0755 FILE-EXTRA/dnfdrake -t %{buildroot}/%{_bindir}/


# data files - OK
install -Dm 0644 FILE-EXTRA/dnfdrake-*-* -t %{buildroot}/%{_datadir}/dnfdrake/
install -Dm 0644 FILE-EXTRA/license -t %{buildroot}/%{_datadir}/dnfdrake/
install -Dm 0644 FILE-EXTRA/COPYING* -t %{buildroot}/%{_datadir}/dnfdrake/
install -Dm 0644 FILE-EXTRA/org.freedesktop.policykit.dnfdrake.policy -t %{buildroot}/%{_datadir}/polkit-1/actions/


install -Dm 0644 FILE-EXTRA/dnfdrake-COMMAND -t %{buildroot}/%{_datadir}/dnfdrake/

# logos
install -Dm 0644 LINUX.png -t %{buildroot}/%{_datadir}/dnfdrake/
install -Dm 0644 OMA*.png -t %{buildroot}/%{_datadir}/dnfdrake/

#.desktop - OK
install -Dm 0755 FILE-EXTRA/dnfdrake.desktop -t %{buildroot}/%{_datadir}/applications

# icons
install -Dm 0644 ICONS-EXTRA/* -t %{buildroot}%{_datadir}/dnfdrake/
install -Dm 0644 ICONS-EXTRA/* -t %{buildroot}%{_datadir}/dnfdrake/icons/
install -Dm 0644 dnfdrake.svg -t %{buildroot}%{_iconsdir}/hicolor/scalable/apps/
for d in 16 32 48 64 72 128 256 512
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -scale ${d}x${d} dnfdrake.svg \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/dnfdrake.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -scale 32x32 dnfdrake.svg %{buildroot}%{_datadir}/pixmaps/dnfdrake.xpm
