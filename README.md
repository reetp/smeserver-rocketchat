# smeserver-rocketchat

How to install Rocket Chat on Koozali SME Server

The current wiki page gives a comprehensive manual guide.

https://wiki.contribs.org/Rocket_Chat

This effort aims to reduce the complexity and make managing Rocket Chat easier.

Currently we need to add some things manually, and then use the contrib to easily update various configuration items

Add repos

yum --enablerepo=centos-sclo-rh,epel install nodejs010

scl enable nodejs010 bash

npm -g install inherits

npm -g install n

n 0.10.40

npm -g install forever

exit

* Might be able to simplify the following a little

cd /root
curl -L https://rocket.chat/releases/latest/download -o rocket.chat.tgz

tar zxvf rocket.chat.tgz

mv bundle /opt/Rocket.Chat

cd /opt/Rocket.Chat/programs/server
npm install

yum --enablerepo=reetp install smeserver-rocketchat

Config entries should then be set by default.

http://chat.yourcerver.com:3000


SSL

Make available in a subdomain and using https (this currently may interfere with letsencrypt)

Install the Webapps-common contrib.

To create your sub domain (e.g. https://chat.yourserver.com)

db domains set chat.yourserver.com domain Description "RocketChat" Nameservers internet \
TemplatePath WebAppVirtualHost RequireSSL enabled ProxyPassTarget http://localhost:3000/

The 'ProxyPassTarget' property could also point to another host (IP) that has Rocket.Chat installed, e.g. a virtual SME Server on the same LAN.
In that case, also LDAP and open/close ports have to be taken into consideration. To expand and activate:

signal-event webapps-update

To disable the default access on port 3000, for we now access our chat platform via the subdomain, and for security we close the default access method.

config setprop rocketchat rootURL localhost mailURL localhost access private

signal-event remoteaccess-update

You can now visit Rocket.Chat at https://chat.yourserver.com

Rocket.Chat will notice that the URL that is being used to access Rocket.Chat has been changed, and will propose to change it to the new URL.


