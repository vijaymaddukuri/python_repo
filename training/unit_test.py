import unittest
from sshclient import CustomSSHClient

def sqr_n_cube(value):
    return value ** 2, value ** 3

class TestCaseSSH(unittest.TestCase):
    def test_ssh_client(self):
        ssh = CustomSSHClient('localhost', 22, 'training', 'training')
        op = ssh.check_output('whoami')
        self.assertEqual(op.decode('ascii'), 'training\n')

class CustomCase(unittest.TestCase):
    def test_sucess(self):
        self.assertEqual(sqr_n_cube(5), (25, 125))

    def test_contains(self):
        self.assertIn(25, sqr_n_cube(5))

    def test_failure_demo(self):
        self.assertEqual(sqr_n_cube(3), (9, 27))

if __name__ == '__main__':
    unittest.main()