from heiwa4126.hello import Hello, hello


def test_hello():
    """
    Test case for the hello function.
    """
    result = hello()
    expected = "hello"
    assert result == expected


def test_hello_class():
    """
    Test case for the Hello class.
    """
    h = Hello("hello")
    result = h.say()
    expected = "hello hello"
    assert result == expected
