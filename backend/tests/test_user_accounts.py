import pytest
from src.services.user_accounts_service import delete_user, is_valid_password, create_user, login_user, change_user_password

# is_valid_password tests
def test_password_length():
    '''
    Test that the password validation function correctly identifies passwords that are too short.
    '''
    assert is_valid_password('Short1!') == 'Password must be at least 8 characters long'
    assert is_valid_password('LongEnough1!') == True

def test_password_uppercase():
    '''
    Test that the password validation function correctly identifies passwords that do not contain an uppercase letter.
    '''
    assert is_valid_password('lowercase1!') == 'Password must contain at least one uppercase letter'
    assert is_valid_password('Uppercase1!') == True 

def test_password_lowercase():
    '''
    Test that the password validation function correctly identifies passwords that do not contain a lowercase letter.
    '''
    assert is_valid_password('UPPERCASE1!') == 'Password must contain at least one lowercase letter'
    assert is_valid_password('Uppercase1!') == True

def test_password_digit_or_special():
    '''
    Test that the password validation function correctly identifies passwords that do not contain a digit or special character.
    '''
    assert is_valid_password('NoSpecialCharOrDigit') == 'Password must contain at least one digit or special character'
    assert is_valid_password('ValidPassword1!') == True
    assert is_valid_password('ValidNoSpecialChar1!') == True
    assert is_valid_password('ValidSpecialChar!AndDigit1') == True

# create_user tests
def test_create_user_success():
    '''
    Test that the create_user function correctly creates a new user.
    '''
    assert create_user('testuser', 'testuser@example.com', 'ValidPassword1!') == ({'message': 'User created successfully'}, 201)
    delete_user('testuser', 'ValidPassword1!')  # Clean up after test
    
def test_create_user_duplicate_username():
    '''
    Test that the create_user function correctly handles duplicate usernames.
    '''
    create_user('test_duplicate_user', 'test_duplicate_user@example.com', 'ValidPassword1!')
    assert create_user('test_duplicate_user', 'another_email@example.com', 'AnotherValidPassword1!') == ({'error': 'Username already taken'}, 400)
    delete_user('test_duplicate_user', 'ValidPassword1!')  # Clean up after test

def test_create_user_duplicate_email():
    '''
    Test that the create_user function correctly handles duplicate emails.
    '''
    create_user('duplicate_email_user', 'duplicate_email@example.com', 'ValidPassword1!')
    assert create_user('another_user', 'duplicate_email@example.com', 'AnotherValidPassword1!') == ({'error': 'Email already registered'}, 400)
    delete_user('duplicate_email_user', 'ValidPassword1!')  # Clean up after test

# login_user tests
def test_login_user_success():
    '''
    Test that the login_user function correctly authenticates a user.
    '''
    create_user('login_test_user', 'login_test_user@example.com', 'ValidPassword1!')
    assert login_user('login_test_user', 'ValidPassword1!') == ({'message': 'Login successful'}, 200)
    delete_user('login_test_user', 'ValidPassword1!')  # Clean up after test

def test_login_user_invalid_username():
    '''
    Test that the login_user function correctly handles invalid usernames.
    '''
    assert login_user('nonexistent_user', 'ValidPassword1!') == ({'error': 'Invalid username or password'}, 401)

def test_login_user_invalid_password():
    '''
    Test that the login_user function correctly handles invalid passwords.
    '''
    create_user('login_test_user', 'login_test_user@example.com', 'ValidPassword1!')
    assert login_user('login_test_user', 'InvalidPassword1!') == ({'error': 'Invalid username or password'}, 401)
    delete_user('login_test_user', 'ValidPassword1!')  # Clean up after test

# change_user_password tests
def test_change_user_password_success():
    '''
    Test that the change_user_password function correctly changes a user's password.
    '''
    create_user('change_password_user', 'change_password_user@example.com', 'ValidPassword1!')
    assert change_user_password('change_password_user', 'ValidPassword1!', 'NewValidPassword1!') == ({'message': 'Password changed successfully'}, 200)
    delete_user('change_password_user', 'NewValidPassword1!')  # Clean up after test

def test_change_user_password_invalid_old_password():
    '''
    Test that the change_user_password function correctly handles invalid old passwords.
    '''
    create_user('change_password_user', 'change_password_user@example.com', 'ValidPassword1!')
    assert change_user_password('change_password_user', 'InvalidPassword1!', 'NewValidPassword1!') == ({'error': 'Old password is incorrect'}, 401)
    delete_user('change_password_user', 'ValidPassword1!')  # Clean up after test

def test_change_user_password_invalid_new_password():
    '''
    Test that the change_user_password function correctly handles invalid new passwords.
    '''
    create_user('change_password_user', 'change_password_user@example.com', 'ValidPassword1!')
    assert change_user_password('change_password_user', 'ValidPassword1!', 'InvalidPassword') == ({'error': 'Password must contain at least one digit or special character'}, 400)
    delete_user('change_password_user', 'ValidPassword1!')  # Clean up after test

def test_change_user_password_same_as_old():
    '''
    Test that the change_user_password function correctly handles the case where the new password is the same as the old password.
    '''
    create_user('change_password_user', 'change_password_user@example.com', 'ValidPassword1!')
    assert change_user_password('change_password_user', 'ValidPassword1!', 'ValidPassword1!') == ({'error': 'New password cannot be the same as the old password'}, 400)
    delete_user('change_password_user', 'ValidPassword1!')  # Clean up after test

# delete_user tests
def test_delete_user_success():
    '''
    Test that the delete_user function correctly deletes a user.
    '''
    create_user('delete_test_user', 'delete_test_user@example.com', 'ValidPassword1!')
    assert delete_user('delete_test_user', 'ValidPassword1!') == ({'message': 'User deleted successfully'}, 200)

def test_delete_user_not_found():
    '''
    Test that the delete_user function correctly handles the case where a user is not found.
    '''
    assert delete_user('nonexistent_user', 'ValidPassword1!') == ({'error': 'User not found'}, 404)

def test_delete_user_incorrect_password():
    '''
    Test that the delete_user function correctly handles the case where an incorrect password is provided.
    '''
    create_user('delete_test_user', 'delete_test_user@example.com', 'ValidPassword1!')
    assert delete_user('delete_test_user', 'InvalidPassword1!') == ({'error': 'Incorrect password'}, 401)