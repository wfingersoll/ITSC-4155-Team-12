import flask as fl

print("---------------\nThis is a test!\n---------------")
print(f"Flask is on version: %s " % fl.__version__)

def test_square():
    assert 3**2 == 9

def test_equals():
    assert 11==10