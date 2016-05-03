%define name smeserver-rocketchat
%define version 0.1
%define release 1
Summary: Plugin to enable RocketChat
Name: %{name}
Version: %{version}
Release: %{release}
License: GNU GPL version 2
URL: http://libreswan.org/
Group: SMEserver/addon
Source: %{name}-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 9.0
Requires: libreswan >= 3.16
Requires: rh-python34-python
Requires: rh-mongodb26-mongodb
Requires: rh-mongodb26-mongodb-server
Requires: nodejs010
Requires: GraphicsMagick

AutoReqProv: no

%description
The ultimate Free Open Source Solution for team communications.

%changelog
* Tue May 03 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-1.sme
- Initial build


%prep
%setup

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
rm -f %{name}-%{version}-filelist
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc COPYING" >> %{name}-%{version}-filelist


%clean
cd ..
rm -rf %{name}-%{version}

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%pre
%preun
%post

scl enable nodejs010 bash
npm install -g inherits
npm install -g n
n 0.10.40
npm install -g forever
exit


#/sbin/e-smith/expand-template /etc/rc.d/init.d/masq
#/sbin/e-smith/expand-template /etc/inittab
#/sbin/init q


echo "https://wiki.contribs.org/Rocket_Chat"

%postun
#/sbin/e-smith/expand-template /etc/rc.d/init.d/masq
#/sbin/e-smith/expand-template /etc/inittab
#/sbin/init q