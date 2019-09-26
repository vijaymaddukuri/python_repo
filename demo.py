"""
S3 command to create bucket:

s3cmd -c s3cmd.scaler-1.cfg mb s3://multi-part-test-bucket


Uploading the file in to s3 bucket:

s3cmd -c s3cmd.scaler-1.cfg put file60mb s3://multi-part-test-bucket


Remove object for bucket:

s3cmd -c s3cmd.scaler-1.cfg del s3://multi-part-test-bucket/file60mb


Remove Bucket:

s3cmd -c s3cmd.scaler-1.cfg rb s3://multi-part-test-bucket

Remove flame reports:
sudo rm -rf /opt/ampli/var/flame_reports/*.csv


Start Flame job:

sudo /opt/ampli/bin/flame job start scalerdb_verify

List the flame jobs:

sudo /opt/ampli/bin/flame job list


----
s3cmd -c s3cmd.scaler-1.cfg del s3://multi-part-test-bucket/file60mb
s3cmd -c s3cmd.scaler-1.cfg rb s3://multi-part-test-bucket
s3cmd -c s3cmd.scaler-1.cfg mb s3://multi-part-test-bucket
s3cmd -c s3cmd.scaler-1.cfg put file60mb s3://multi-part-test-bucket


"""



import keyrouter_api.ttypes as kt
from sherpa import cli_wrapper as cli
from keyrouter_api.ttypes import SDB_SpaceEnum_t
from thrift.transport import TTransport
from scalerdb_api.common.ttypes import SDB_KeyOption
from scalerdb_api.values.ttypes import SDB_BucketId, SDB_Object
from scaler_python_utils.thrift.TCompatibleCompactProtocol import TCompatibleCompactProtocol
from scaler_api import scalerdb as utils




list_bucket_entries = cli.clients.keyrouter.listEntries("list_bucket", SDB_SpaceEnum_t.BUCKET_SPACE, SDB_KeyOption("Nmulti-part-test-bucket"), SDB_KeyOption("Nmulti-part-test-bucket"),1)
t = TTransport.TMemoryBuffer(list_bucket_entries.entries[0].value.blob)
p = TCompatibleCompactProtocol(t)
sdb_bucket_id = SDB_BucketId()
sdb_bucket_id.read(p)
prefix = sdb_bucket_id.id
list_result = cli.clients.keyrouter.listEntries3("flametest", "", None, SDB_SpaceEnum_t.OBJECT_SPACE, prefix, prefix, False, None, 1000)

## TC1 Validate the multi part object by deleting one part of the object.

original_bucket = cli.clients.keyrouter.remove("", kt.SDB_SpaceEnum_t.OBJECT_SPACE, list_result.entries[4].key)

## TC2 Validate the multi part object by changing the size of the main object.

prefix = list_result.entries[0].key
p_key=prefix.split("file60mb")
prefix=p_key[0]+"file60mb"
entries = cli.clients.keyrouter.listEntries2a('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, '', '', False, prefix, 10, None, False)
okey = entries.entries[0].key
oval = entries.entries[0].value
obj = utils.deserialize_blob_of_sdb_value(oval)
initial_size_of_obj = obj.multipartMetaData.size
obj.multipartMetaData.size = initial_size_of_obj+1
mobj_blob = utils.serialize(obj)
modified_obj_sdb_val = oval
modified_obj_sdb_val.blob = mobj_blob
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, okey, modified_obj_sdb_val)

# TC3 Validate the multi part object by changing the size of one part object.

prefix = list_result.entries[4].key
entries = cli.clients.keyrouter.listEntries2a('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, '', '', False, prefix, 10, None, False)
okey = entries.entries[0].key
oval = entries.entries[0].value
obj = utils.deserialize_blob_of_sdb_value(oval)
initial_size_of_obj = obj.singlePart.size
obj.singlePart.size = initial_size_of_obj+1
mobj_blob = utils.serialize(obj)
modified_obj_sdb_val = oval
modified_obj_sdb_val.blob = mobj_blob
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, okey, modified_obj_sdb_val)


# TC4 Validate the multi part object by changing the etag of one part object
pkey = list_result.entries[4].key
value = cli.clients.keyrouter.get('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)
pobj = utils.deserialize_blob_of_sdb_value(value.value)
checksum = list(pobj.singlePart.checksum)
checksum[-2] = 1
checksum=bytearray(checksum)
pobj.singlePart.checksum=checksum
mval = value.value
modified_pblob = utils.serialize(pobj)
mval.blob = modified_pblob
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey, mval)

# TC5 Validate the multi part object by changing dbkey type of one part object.
pkey = list_result.entries[4].key
pvalue = list_result.entries[4].value
temp=list(pkey)
temp[-4]=1
mkey = bytearray(temp)
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, mkey, pvalue)
cli.clients.keyrouter.remove('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)

# TC6 Validate the multi part object by byte filp for one key of MP object.
pkey = list_result.entries[4].key
pvalue = list_result.entries[4].value
temp=list(pkey)
temp[-28]="v"
mkey = bytearray(temp)
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, mkey, pvalue)
cli.clients.keyrouter.remove('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)

# TC7 Validate the multi part object by modifying upload id of one part key of MP object.
pkey = list_result.entries[4].key
pvalue = list_result.entries[4].value
temp=list(pkey)
temp[-30]=1
mkey = bytearray(temp)
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, mkey, pvalue)
cli.clients.keyrouter.remove('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, pkey)


# TC8 Validate the multiple versions of an MP object by changing the size of one part object.

prefix = list_result.entries[0].key
entries = cli.clients.keyrouter.listEntries2a('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, '', '', False, prefix, 10, None, False)
okey = entries.entries[0].key
oval = entries.entries[0].value
obj = utils.deserialize_blob_of_sdb_value(oval)
initial_size_of_obj = obj.multipartMetaData.size
obj.multipartMetaData.size = initial_size_of_obj+1
mobj_blob = utils.serialize(obj)
modified_obj_sdb_val = oval
modified_obj_sdb_val.blob = mobj_blob
cli.clients.keyrouter.put('', kt.SDB_SpaceEnum_t.OBJECT_SPACE, okey, modified_obj_sdb_val)
print(prefix.encode('base64', 'strict'))
