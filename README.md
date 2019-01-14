# smeserver-rocketchat

How to install Rocket Chat on Koozali SME Server (this only works up to Rocket 0.39 - I am currently working on an update)

The current wiki page gives a comprehensive manual guide.

https://wiki.contribs.org/Rocket_Chat

This effort aims to reduce the complexity and make managing Rocket Chat easier.

Currently we need to add some things manually, and then use the contrib to easily update various configuration items

Rocket

Add repos:

https://wiki.contribs.org/User:ReetP

epel
centos-sclo-sh
reetp 

yum install scl-utils rh-python34-python rh-mongodb26-mongodb rh-mongodb26-mongodb-server GraphicsMagick --enablerepo=centos-sclo-rh,epel


yum --enablerepo=centos-sclo-rh install rh-mongodb30upg,rh-mongodb32



Old way - we now use docker as we can't compile various modules on CentOS 6 very easily



cd /opt/Rocket.Chat/programs/server
npm install -g forever fibers underscore source-map-support semver

You will have to make sure that you get a version no later than 0.39)

cd /root
curl -L https://rocket.chat/releases/latest/download -o rocket.chat.tgz
tar zxvf rocket.chat.tgz
mv bundle /opt/Rocket.Chat

patch mailcomposer.js to add From header. You can use this from wherever the patch file is (currently in /opt):
cd /opt
patch -p0 -i mailcomposer.patch

Install smeserver-rocketchat contrib

yum enablerepo=reetp install smeserver-rocketchat

db setprop rocketchat status enabled

signal-event post-upgrade;signal-event reboot

rocketchat=service
    TCPPort=3000
    access=public
    mailPort=25
    mailURL=localhost
    status=enabled

rh-mongodb26-mongod=service
    TCPPort=27017
    access=private
    mongoURL=localhost
    status=enabled

BEFORE we login for the first time we need to set up mail settings correctly:

From bash
mongo rocketchat --eval 'db.rocketchat_settings.update({"_id" : "SMTP_Host"}, {$set: {"value":"localhost"}});'
mongo rocketchat --eval 'db.rocketchat_settings.update({"_id" : "From_Email"}, {$set: {"value":"admin@yourdomain.com"}});'

We can check the individual values set like this:

mongo rocketchat --eval 'db.rocketchat_settings.find({"_id":"From_Email"}, {_id:0, value:1}).shellPrint();'
mongo rocketchat --eval 'db.rocketchat_settings.find({"_id":"SMTP_Host"}, {_id:0, value: 1}).shellPrint();'

All values per _id:
mongo rocketchat --eval 'db.rocketchat_settings.find({"_id" : "SMTP_Host"}).shellPrint();'
mongo rocketchat --eval 'db.rocketchat_settings.find({"_id" : "From_Email"}).shellPrint();'

Now restart rocketchat to reread the DB settings:

service rocketchat restart

Login at http://yourdomain:3000

It will first get you to create an admin user. 

If you have an issue with no email sent/received then login using the email address and password you just set

Look for bugs :-)



Using mongo itself to modify the DB:

mongo
use rocketchat
db.rocketchat_settings.find({"_id" : "SMTP_Host"})
db.rocketchat_settings.find({"_id" : "From_Email"})

db.rocketchat_settings.findOne({_id:'From_Email'}, {_id:0, value: 1})
db.rocketchat_settings.findOne({_id:'SMTP_Host'}, {_id:0, value: 1})


db.rocketchat_settings.update({"_id" : "From_Email"}, {$set: {"value":"admin@reetspetit.info"}})
db.rocketchat_settings.update({"_id" : "SMTP_Host"}, {$set: {"value":"mail.reetspetit.info"}})


SSL / Proxies

This is still experimental !

Make available in a subdomain and using https (this currently may interfere with letsencrypt)

To create your sub domain (e.g. https://chat.yourserver.com)

db domains set chat.yourserver.com domain Description "RocketChat" Nameservers internet \
TemplatePath ProxyPassVirtualRocketchat RequireSSL enabled ProxyPassTarget http://localhost:3000/

The 'ProxyPassTarget' property could also point to another host (IP) that has Rocket.Chat installed, e.g. a virtual SME Server on the same LAN.
In that case, also LDAP and open/close ports have to be taken into consideration. 

signal-event remoteaccess-update

To disable the default access on port 3000, for we now access our chat platform via the subdomain, and for security we close the default access method.

config setprop rocketchat rootURL localhost mailURL localhost access private

signal-event remoteaccess-update

You can now visit Rocket.Chat at https://chat.yourserver.com

Rocket.Chat will notice that the URL that is being used to access Rocket.Chat has been changed, and will propose to change it to the new URL.


