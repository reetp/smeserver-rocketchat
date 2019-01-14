%define name smeserver-rocketchat
%define version 0.2
%define release 3
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
Requires: e-smith-release >= 9.2
Requires: rh-python34-python
Requires: rh-mongodb26-mongodb-server
Requires: rh-mongodb30upg-mongodb-server
Requires: rh-mongodb32-mongodb-server
#Requires: nodejs >= 4.8
#Requires: GraphicsMagick
Requires: mod_proxy_wstunnel >= 0.1
Requires: smeserver-docker

AutoReqProv: no

%description
The ultimate Free Open Source Solution for team communications.

%changelog
* Mon Jan 14 2019 John Crisp <jcrisp@safeandsoundit.co.uk> 0.2-3.sme
- Add service links

* Mon Jan 14 2019 John Crisp <jcrisp@safeandsoundit.co.uk> 0.2-2.sme
- remove old rocketchat service now we use docker
- add settings for mongodb30upg and mongodb32

* Fri Aug 17 2018 John Crisp <jcrisp@safeandsoundit.co.uk> 0.2-1.sme
- Move to using Docker

* Tue Jan 09 2018 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-15.sme
- Update SME Version
- Update node version
- Fix missing quote

* Thu Jul 27 2017 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-14.sme
- Proxy template does not work on Apache 2.2
- Revised proxy templates that also work with letsencrypt

* Thu Jun 01 2017 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-13.sme
- Update httpd proxy template as per recommendation
- https://rocket.chat/docs/installation/manual-installation/configuring-ssl-reverse-proxy

* Thu Apr 20 2017 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-12.sme
- Add new kill links
- Add log rotate
- bump nodejs requires for newer version of rocketchat
- mailcomposer patch removed as this is now in Meteor
- Remove mongo service createlinks

* Wed Dec 21 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-11.sme
- Fix incorrect link in createlinks

* Tue Dec 20 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-10.sme
- Fix incorrect logrotate template location

* Tue Dec 20 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-9.sme
- Fix incorrect curly brace in 20variables

* Thu Nov 24 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-8.sme
- Modify SSL Support
- Add SSLProxy key

* Wed Nov 23 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-7.sme
- add logrotate template
- Remove /home from http redirect

* Tue Oct 31 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-6.sme
- Update for Rocket v0.40+ allowing for higher version of node

* Fri Aug 26 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-5.sme
- Fix Proxy pass for letsencrypt

* Tue Aug 16 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-4.sme
- Add SSL / proxy support

* Mon Aug 15 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-3.sme
- Small fixes

* Mon Aug 15 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-2.sme
- Lots of changes to scripts an file locations

* Tue May 06 2016 John Crisp <jcrisp@safeandsoundit.co.uk> 0.1-1.sme
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

# if exists remove the following
if [[ -f /etc/e-smith/templates/etc/profile.d/scls-nodejs010.sh ]];
then rm -f /etc/e-smith/templates/etc/profile.d/scls-nodejs010.sh;
fi

if [[ ! -e /etc/profile.d/scls-nodejs010.sh ]];
then rm -f /etc/profile.d/scls-nodejs010.sh;
fi

# Need to clean old symlinks

rm -f /etc/rc.d/rc0.d/K21rh-mongodb26-mongod 2> /dev/null
rm -f /etc/rc.d/rc1.d/K21rh-mongodb26-mongod 2> /dev/null
rm -f /etc/rc.d/rc6.d/K21rh-mongodb26-mongod 2> /dev/null

rm -f /etc/rc.d/rc0.d/K21rocketchat 2> /dev/null
rm -f /etc/rc.d/rc1.d/K21rocketchat 2> /dev/null
rm -f /etc/rc.d/rc6.d/K21rocketchat 2> /dev/null

echo "****************************************"
echo "https://wiki.contribs.org/Rocket_Chat"

echo "****************************************"

%postun
