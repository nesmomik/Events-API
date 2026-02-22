# unit tests
# test only the class logic, no database needed
from models import User

def test_set_and_check_password():
    '''test the password checking logic'''
    # arrange: create user and set password
    user = User(username = "test")
    user.set_password("test")

    # act & assert: check user password
    assert user.check_password("test")
