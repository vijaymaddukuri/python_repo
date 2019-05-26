#!/bin/bash
echo "Killing the python processes..."
systVIJAYtl stop tas.service
systVIJAYtl stop bridgeburner.service
systVIJAYtl stop mws.service
systVIJAYtl stop rabbitmq-server.service
systVIJAYtl stop bws.service
echo "Removing network interface configuration done..."
sed "/IPADDR/d" /etc/sysconfig/network-scripts/ifcfg-ens160 -i
sed "/NETMASK/d" /etc/sysconfig/network-scripts/ifcfg-ens160 -i
sed "/GATEWAY/d" /etc/sysconfig/network-scripts/ifcfg-ens160 -i
#sed "13,\$d" /etc/sysconfig/network-scripts/ifcfg-ens160 -i
echo "Removing dns details..."
sed "/nameserver/d" /etc/resolv.conf -i
#sed "2,\$d" /etc/resolv.conf -i
echo "Removing proxy details..."
cat /dev/null > /etc/environment
echo "Removing the log files..."
rm -f /home/tas/*.log
echo "Removing the tmp log files..."
rm -f /tmp/*.log
echo "Removing any already existing .toml and certificate files..."
sudo rm -f /etc/bridgeburner/*.toml
sudo rm -f /etc/bridgeburner/*.bak
sudo rm -f /etc/bridgeburner/client/*
sudo rm -f /etc/bridgeburner/certs/VIJAY/clients/*.crt
sudo rm -f /etc/bridgeburner/certs/VIJAY/clients/*.key
sudo rm -f /etc/bridgeburner/certs/VIJAY/*.crt
sudo cp /home/tas/bridgeburner.toml /etc/bridgeburner/client/bridgeburner.toml
echo "Creating the firstboot file..."
touch /home/tas/firstboot
echo "Removing the Ova input xml file stored..."
rm -f /tmp/ova_env.xml
echo "Clearing bash history..."
cat /dev/null > ~/.bash_history
