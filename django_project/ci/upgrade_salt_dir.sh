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

yes | cp -Rf salt_artifacts/netapi/*  /srv/install/

if [ $? -ne 0 ]; then { echo "Unable to copy the netapi repo, aborting." ; exit 1; } fi

yes | cp -Rf salt/install/* /srv/install/

if [ $? -ne 0 ]; then { echo "Unable to copy salt installation files, aborting." ; exit 1; } fi

search=$(perl -0777 -ne 'while(m/\bfile_roots:\s+base:\s+\-\s\/srv\/salt\/tsa/g){print "$&\n";}' /etc/salt/master)

if [[ -z "$search" ]]; then
   perl -0777 -pi -e 's/(file_roots:\s+base:)/$1\n    - \/srv\/salt\/tsa/' /etc/salt/master
   echo "Added tsa repo in master config file"
fi


