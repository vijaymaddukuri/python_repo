import jmespath
import json

input1 = '''{
  "machines": [
    {"name": "a", "state": "running"},
    {"name": "b", "state": "stopped"},
    {"name": "b", "state": "running"}
  ]
}'''

jsonData = """{
  "products" : {
    "DQ578CGN99KG6ECF" : {
      "sku" : "DQ578CGN99KG6ECF",
      "productFamily" : "Compute",
      "attributes" : {
        "location" : "US East (N. Virginia)",
        "instanceType" : "hs1.8xlarge",
        "tenancy" : "Shared",
        "operatingSystem" : "Windows",
        "licenseModel" : "License Included",
        "preInstalledSw" : "NA"
      }
    },
    "G2N9F3PVUVK8ZTGP" : {
      "sku" : "G2N9F3PVUVK8ZTGP",
      "productFamily" : "Instance",
      "attributes" : {
        "location" : "Asia Pacific (Seoul)",
        "instanceType" : "i2.xlarge",
        "tenancy" : "Host",
        "operatingSystem" : "Windows",
        "licenseModel" : "License Included",
        "preInstalledSw" : "SQL Server Enterprise"
      }
    },
    "FBZZ2TKXWWY5HZRX" : {
      "sku" : "FBZZ2TKXWWY5HZRX",
      "productFamily" : "Compute",
      "attributes" : {
        "location" : "Asia Pacific (Seoul)",
        "instanceType" : "i2.4xlarge",
        "tenancy" : "Dedicated",
        "operatingSystem" : "SUSE",
        "licenseModel" : "No License required",
        "preInstalledSw" : "NA"
      }
    }
  }
}"""


priceJson = json.loads(input1)
query= "machines[?state=='running'].name"
print(jmespath.search(query,priceJson))

priceJson = json.loads(jsonData)

query = "products.*.{sku: sku, location: attributes.location, instanceType: attributes.instanceType, tenancy: attributes.tenancy, operatingSystem: attributes.operatingSystem, licenseModel: attributes.licenseModel, preInstalledSw: attributes.preInstalledSw}"
output_dict = jmespath.search(query, priceJson)

query2 = "[?operatingSystem=='Windows' && tenancy=='Shared']"
output_dict = jmespath.search(query2, output_dict)

print(output_dict)