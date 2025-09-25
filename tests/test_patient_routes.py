# Mocked tests for demo repo
# Simple unittest structure to make the repo look realistic for SCA and CI analyses.

import unittest

class DummyTests(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
