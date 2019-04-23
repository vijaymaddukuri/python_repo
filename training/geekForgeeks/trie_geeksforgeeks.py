import string
import random

class TrieNode: 
      
    # Trie node class 
    def __init__(self): 
        self.children = [None]*26
  
        # isEndOfWord is True if node represent the end of the word 
        self.isEndOfWord = False
  
class Trie: 
      
    # Trie data structure class 
    def __init__(self): 
        self.root = self.getNode() 
  
    def getNode(self): 
      
        # Returns new trie node (initialized to NULLs) 
        return TrieNode() 
  
    def _charToIndex(self,ch): 
          
        # private helper function 
        # Converts key current character into index 
        # use only 'a' through 'z' and lower case 
          
        return ord(ch)-ord('a') 
  
  
    def insert(self,key): 
          
        # If not present, inserts key into trie 
        # If the key is prefix of trie node,  
        # just marks leaf node 
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
  
            # if current character is not present 
            if not pCrawl.children[index]: 
                pCrawl.children[index] = self.getNode() 
            pCrawl = pCrawl.children[index] 
  
        # mark last node as leaf 
        pCrawl.isEndOfWord = True
  
    def search(self, key): 
          
        # Search key in the trie 
        # Returns true if key presents  
        # in trie, else false 
        pCrawl = self.root 
        length = len(key) 
        for level in range(length): 
            index = self._charToIndex(key[level]) 
            if not pCrawl.children[index]: 
                return False
            pCrawl = pCrawl.children[index] 
  
        return pCrawl != None and pCrawl.isEndOfWord

    def get_first_level_words(self):
        s = set()
        root = self.root
        for child in root.children:
            if child is not None:
                s.add()

class Boggle:
    def __init__(self, dictionary, size=4):
        self.dictionary = dictionary
        self.size = size
        self.n = self.size * self.size
        self.__initialize_board()

    def __initialize_board(self):
        self.cells = [""]*(self.n)
        for i in range(self.n):
            self.cells[i] = random.choice(string.ascii_lowercase)

    def display_board(self):
        n = self.n
        width = self.width
        i = 0
        while i < n:
            row_content = ""
            for j in range(width):
                row_content += self.cells[i] + " |"
                i += 1
            print(row_content)
            row_len = len(row_content)
            dashes = '-' * (row_len)
            print(dashes)

    def find_all_words(self):
        dictionary.get_first_level_words()

# driver function 
def main(): 
  
    # Input keys (use only 'a' through 'z' and lower case) 
    keys = ["the","a","there","anaswe","any", 
            "by","their"]
         
    output = ["Not present in trie", 
              "Present in tire"] 
  
    # Trie object 
    t = Trie() 
  
    # Construct trie 
    with open("words.txt") as f:
        for line in f:
            t.insert(line) 
  
    # Search for different keys 
    print("{} ---- {}".format("the",output[t.search("the")])) 
    print("{} ---- {}".format("these",output[t.search("these")])) 
    print("{} ---- {}".format("their",output[t.search("their")])) 
    print("{} ---- {}".format("thaw",output[t.search("thaw")])) 
  
if __name__ == '__main__': 
    main()
