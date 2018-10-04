import io
import unittest

from training.unit_testing.fake_object_example import FileOpen


class FileTest(unittest.TestCase):
    def test_file_open(self):
        # filename = os.path.join(tempfile.gettempdir(), "aflie.txt")
        read = FileOpen(FakeFileWrapper("vijay"))
        read = (read.get_item())
        self.assertEqual("vijay", read)


class FakeFileWrapper:
    def __init__(self, text):
        self.text = text

    def open(self):
        return  io.StringIO(self.text)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

# input_value = FileOpen(FakeFileWrapper("test test"))
# print(input_value.get_item())


