#
# spec file for package pcsc-ccid
#
# Copyright (c) 2020 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           pcsc-ccid
Version:        1.4.35
Release:        0
Summary:        PCSC Driver for CCID Based Smart Card Readers and GemPC Twin Serial Reader
License:        LGPL-2.1-or-later
Group:          Productivity/Security
URL:            https://ccid.apdu.fr/
Source:          %{name}-%{version}.tar.bz2
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  libtool
BuildRequires:  flex
BuildRequires:  libusb1-devel
BuildRequires:  pcsc-lite-devel
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(udev)
# openSUSE package pcsc-lite 1.6.6 is the first one which creates the scard UID and GID:
Requires:       pcsc-lite >= 1.6.6
%define ifddir %(pkg-config libpcsclite --variable=usbdropdir)

#%# We are not using Supplements here. User may want to choose between pcsc-lite and openct:
# Generic CCID devices:
Enhances:       modalias(usb:*ic0Bisc00d*dc*dsc*dp*ic*isc*ip*)
# Kobil mIDentity:
Enhances:       modalias(usb:v0D46p4081d*dc*dsc*dp*ic*isc*ip*)

%description
This package contains a generic USB CCID (Chip/Smart Card Interface
Devices) driver.

This driver is meant to be used with the PCSC-Lite daemon from the
pcsc-lite package.

%prep
%setup -q -n %{name}-%{version}/CCID
cp -a src/openct/LICENSE LICENSE.openct
cp -a src/towitoko/README README.towitoko

%build
%reconfigure\
    --enable-twinserial \
    --enable-zlp \
    --enable-serialconfdir=%{_sysconfdir}/reader.conf.d/
%make_build

%install
%make_install
mkdir -p %{buildroot}/%{_udevrulesdir}
sed 's:GROUP="pcscd":GROUP="scard":' <src/92_pcscd_ccid.rules >%{buildroot}/%{_udevrulesdir}/92_pcscd_ccid.rules

%files
%defattr(-,root,root)
%doc AUTHORS README.md README.towitoko contrib/Kobil_mIDentity_switch/README_Kobil_mIDentity_switch.txt SCARDGETATTRIB.txt
%license COPYING LICENSE.openct
%config (noreplace) %{_sysconfdir}/reader.conf.d/*
%{ifddir}/*
%{_udevrulesdir}/*.rules

%changelog
