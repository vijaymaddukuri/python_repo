from psdirlisting import DirectoryListing
from json import dump

class DirectoryListingToJSON(DirectoryListing):
    def to_json(self, json_file):
        dump(self.container, open(json_file, 'w'), indent=4)

if __name__ == '__main__':
    dl = DirectoryListingToJSON(r'c:\users\madduv\Desktop')
    dl.to_json(r'C:\Users\madduv\Desktop\tmp.json')