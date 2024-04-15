import unittest

from heiwa4126.hello import hello


class TestHello(unittest.TestCase):
    """
    A test case for the hello function.
    """

    def test_hello(self):
        """
        Test case for the hello function.
        """
        result = hello()
        expected = "hello"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
