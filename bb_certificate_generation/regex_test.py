import re

# Update toml file

fname = "bridgeburner.toml"

# Read in the file
with open(fname, 'r') as file:
    filedata = file.read()

output = filedata
client_cert_list=['VIJGF-backup-automation.crt', 'VIJGF-backup-automation.key']
bbserver_ip='10.100.249.49'
client_ip='10.100.249.47'
tenant_id='3512ea87-4116-4e83-b8cc-8687cf129972'


cername = "certFile=\"/etc/bridgeburner/certs/Virtustream/clients/{}\"".format(client_cert_list[0])
keyname = "keyFile=\"/etc/bridgeburner/certs/Virtustream/clients/{}\"".format(client_cert_list[1])
server = "serverAddress=\"{}:7000\"".format(bbserver_ip)
bb_client = "Address=\"{}\"".format(client_ip)
ten_id = "Name=\"{}\"".format(tenant_id)

output = re.sub("certFile=\"/etc/bridgeburner/certs/Virtustream/clients/\S+.crt\"", cername, output)
output = re.sub("keyFile=\"/etc/bridgeburner/certs/Virtustream/clients/\S+.key\"", keyname, output)
output = re.sub("serverAddress=\"\S+\"", server, output)
output = re.sub("\sAddress=\"\S+\"", " " + bb_client, output)
output = re.sub("Name=\"\S+\"", ten_id, output)

with open(fname, 'w') as f:
    f.write(output)
