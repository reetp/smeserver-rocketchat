[root@test ipsec.d]# cat /root/rocketupdate.sh
#!/bin/bash
cd /root
curl -L https://rocket.chat/releases/0.44.0/download -o rocket.chat.tgz
tar zxvf rocket.chat.tgz
service rocketchat stop
cd /opt
mv Rocket.Chat Rocket.Chat.0.43.0
cd ~
mv bundle /opt/Rocket.Chat
cd /opt
npm install forever fibers underscore source-map-support semver module
node main.js
service rocketchat restart
