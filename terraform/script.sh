Content-Type: multipart/mixed; boundary="//"
MIME-Version: 1.0

--//
Content-Type: text/cloud-config; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="cloud-config.txt"

#cloud-config
cloud_final_modules:
- [scripts-user, always]

--//
Content-Type: text/x-shellscript; charset="us-ascii"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Content-Disposition: attachment; filename="userdata.txt"

#!/bin/bash
echo "START SETUP" >> /tmp/log.txt
sudo apt-get -y update
sudo apt-get -y install \
ca-certificates \
curl \
gnupg \
lsb-release
sudo apt -y install unzip
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get -y update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo chmod 666 /var/run/docker.sock
sudo apt install make
echo 'Clone git repo to EC2' >> /tmp/log.txt
fucking private repo!!!!!
cd /home/ubuntu && git clone https://github.com/vladimirryzhikov/Project_DE_15_03_23
echo 'CD to Project directory' >> /tmp/log.txt
cd Project_DE_15_03_23 
echo 'Start containers' >> /tmp/log.txt
echo "/* make up (run this after adding containers) */" >> /tmp/log.txt
echo "____________END SETUP______" >> /tmp/log.txt
--//--