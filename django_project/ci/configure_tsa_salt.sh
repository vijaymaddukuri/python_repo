#!/bin/bash
show_usage() {
    echo "usage: $0 [-u username] [-p password] [-s port]"
    echo "  -u | --username <username>   username of new user to be create"
    echo "  -p | --password <password>   password of new user"
    echo "  -s | --port <Port number>    The port for the webserver to listen on."
}


if [[ "$1" =~ ^((-{1,2})([Pp])|)$ ]]; then
  show_usage; exit 1
else
  while [[ $# -gt 0 ]]; do
    opt="$1"
    shift;
    current_arg="$1"
    if [[ "$current_arg" =~ ^-{1,2}.* ]]; then
      echo "WARNING: You may have left an argument blank. Double check your command."
    fi
    case "$opt" in
      "-u"|"--username"      ) username="$1"; shift;;
      "-p"|"--password"      ) password="$1"; shift;;
      "-s"|"--port"          ) port="$1"; shift;;
      *                      ) echo "ERROR: Invalid option: \""$opt"\"" >&2
                            exit 1;;
    esac
  done
fi

if [[ "$username" == "" || "$password" == "" ]]; then
  echo "ERROR: Options -u and -p require arguments." >&2
  exit 1
fi
if [ -z "$username" ]
then
        echo "Username is required."
    show_usage
        exit 2
fi
if [ -z "$password" ]
then
        echo "Password is required."
    show_usage
        exit 2
fi
if [ -z "$port" ]
then
       port=8000
fi

mkdir -p /srv/salt/tsa/
yes | cp -Rf salt/* /srv/salt/tsa/
mkdir -p /srv/install/
if [ $? -ne 0 ]; then { echo "Unable to copy the salt files, aborting." ; exit 1; } fi

mkdir -p /srv/pillar/tsa/
yes | cp -Rf pillar/* /srv/pillar/tsa/

if [ $? -ne 0 ]; then { echo "Unable to copy the pillar files, aborting." ; exit 1; } fi

mkdir -p /srv/salt/tsa/REPO/networker
yes | cp -Rf salt_artifacts/networker/* /srv/salt/tsa/REPO/networker/

if [ $? -ne 0 ]; then { echo "Unable to copy the networker repo, aborting." ; exit 1; } fi

mkdir -p /srv/salt/tsa/REPO/Nimsoft-install/nimldr
yes | cp -Rf salt_artifacts/nimsoft/* /srv/salt/tsa/REPO/Nimsoft-install/nimldr/

if [ $? -ne 0 ]; then { echo "Unable to copy the nimsoft repo, aborting." ; exit 1; } fi


cp -R salt/install/template_tsa.conf /etc/salt/master.d/tsa.conf

if [ $? -ne 0 ]; then { echo "Unable to copy the tas conf file, aborting." ; exit 1; } fi
current_dir=`pwd`
cd salt_artifacts/netapi
for x in *.rpm; do
        installedbinary=`basename $x .rpm`
        if [ `rpm -qa|grep -c $installedbinary` -ne 0 ]; then
            echo "$x already installed, hence removing";
            rm $x;
        else
            echo $x :"Not installed";
        fi
done
for d in */; do
        cd $d
         for x in *.rpm; do
           installedbinary=`basename $x .rpm`
           if [ `rpm -qa|grep -c $installedbinary` -ne 0 ]; then
             echo "$x already installed, hence removing";
             rm $x;
           else
             echo $x :"Not installed";
           fi
         done
         cd ..
done
cd $current_dir
yes | cp -Rf salt_artifacts/netapi/*  /srv/install/

if [ $? -ne 0 ]; then { echo "Unable to copy the netapi repo, aborting." ; exit 1; } fi

yes | cp -Rf salt/install/* /srv/install/

if [ $? -ne 0 ]; then { echo "Unable to copy salt installation files, aborting." ; exit 1; } fi

search=$(perl -0777 -ne 'while(m/\bfile_roots:\s+base:\s+\-\s\/srv\/salt\/tsa/g){print "$&\n";}' /etc/salt/master)

if [[ -z "$search" ]]; then
   perl -0777 -pi -e 's/(file_roots:\s+base:)/$1\n    - \/srv\/salt\/tsa/' /etc/salt/master
   echo "Added tsa repo in master config file"
fi

cd /srv/install

chmod +x install_rest_cherrypy.sh

./install_rest_cherrypy.sh -u $username -p $password -s $port

if [ $? -ne 0 ]; then { echo "Unable to execute rest cherrypy script, aborting." ; exit 1; } fi

