'''WeConnect Users Test File'''
import unittest
import json
from app import app
class UserendpointsTestcase(unittest.TestCase):
    '''User endpoints test class'''
    def setUp(self):
        self.app = app.test_client(self)
        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="kelvin@live", username="kelvin",
                                           password="12345678")), content_type="application/json")

        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="ed@live", username="ed",
                                           password="12345678")), content_type="application/json")
        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="dee@live", username="dee",
                                           password="12345678")), content_type="application/json")

        self.user = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="kelvin", password="12345678")),
                                 content_type="application/json")
        self.access_token = json.loads(self.user.data.decode())['access_token']

        self.user = self.app.post("/api/v1/auth/login",
                             data=json.dumps(dict(username="ed", password="12345678")),
                             content_type="application/json")

        self.user2 = self.app.post("/api/v1/auth/login",
                             data=json.dumps(dict(username="dee", password="12345678")),
                             content_type="application/json")                                           

    def test_user_register(self):
        '''Test User Registration method'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live", username="nina",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "User Succesfully Registered")

    def test_email_not_empty(self):
        '''Test for blank email input'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="", username="nina",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['email-Error:']['message'], "email cannot be an empty string")

    def test_username_not_empty(self):
        '''Test for blank username input'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live", username="",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        print(response_msg)
        self.assertEqual(response_msg['username-Error:']['message'],
                         "username cannot be an empty string")
    def test_password_not_empty(self):
        '''Test for blank password'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live.com", username="nina",
                                                      password="")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']["message"],
                         "password cannot be an empty string")

    def test_missing_email(self):
        '''Test for missing email'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(username="nina",
                                                      password="12345")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['email-Error:']["message"],
                         "email cannot be missing")

    def test_register_missing_username(self):
        '''Test for missing username'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live.com",
                                                      password="12345")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']["message"],
                         "username cannot be missing")

    def test_register_missing_password(self):
        '''Test for missing password'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live.com",
                                                      username="12345")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']["message"],
                         "password cannot be missing")

    def test_user_register_whitespace(self):
        '''Test User Registration method'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live", username="ni na",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Username cannot contain white spaces")

    def test_email_already_registered(self):
        '''Test for existing email'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="kelvin@live", username="kelin",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Email already existing.")

    def test_username_exists(self):
        '''test for existing username'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="kev@live", username="kelvin",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Username already existing.")
    def test_user_login_empty_username(self):
        '''Test for blank username input'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']["message"],
                                      "username cannot be an empty string")
    def test_user_login_empty_password(self):
        '''Test for blank password input'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="kelvin",
                                                      password="")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']["message"],
                                      "password cannot be an empty string")

    def test_login_missing_username(self):
        '''Test for missing username'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(password="12345")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['username-Error:']["message"],
                         "username cannot be missing")

    def test_login_missing_password(self):
        '''Test for missing password'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="nina")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['password-Error:']["message"],
                         "password cannot be missing")
    def test_user_login(self):
        '''Test for login'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="kelvin", password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "You are logged in successfully")
        self.assertTrue(response_msg['access_token'])

    def test_wrong_password(self):
        '''Test for wrong password'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="kelvin", password="123678")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Wrong password")
    def test_non_existing_user(self):
        '''Test for non-existing user'''
        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="melvin", password="12345678")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Non-existent user. Try signing up")


    def test_reset_missing_old_password(self):
        '''Test for missing old password'''
        response = self.app.post("/api/v1/auth/reset-password",
                                 data=json.dumps(dict(new_password="12345667")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['old_password-Error:']["message"],
                         "old_password cannot be missing")

    def test_reset_missing_new_password(self):
        '''Test for missing new password'''
        response = self.app.post("/api/v1/auth/reset-password",
                                 data=json.dumps(dict(old_password="12345667")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['new_password-Error:']["message"],
                         "new_password cannot be missing")
    def test_password_reset(self):
        '''Test for password reset'''
        access_token = json.loads(self.user.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/reset-password",
                                 data=json.dumps(dict(old_password="12345678",
                                                      new_password="12345")),
                                 headers={
                                     "Authorization": "Bearer {}".format(access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Reset successful")
    def test_login_after_password_reset(self):
        '''Test for login after reset'''
        access_token = json.loads(self.user2.data.decode())['access_token']

        self.app.post("/api/v1/auth/reset-password",
                      data=json.dumps(dict(old_password="12345678",
                                           new_password="12345")),
                      headers={
                          "Authorization": "Bearer {}".format(access_token),
                          "Content-Type": "application/json"
                          })

        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="dee", password="12345")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "You are logged in successfully")
    def test_wrong_password_reset(self):
        '''Test for wrong old password in reset'''
        user = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="ed", password="12345")),
                                 content_type="application/json")

        access_token = json.loads(user.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/reset-password",
                                 data=json.dumps(dict(old_password="12345667",
                                                      new_password="12345!@")),
                                 headers={
                                     "Authorization": "Bearer {}".format(access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],
                         "Wrong Password. Cannot reset. Forgotten password?")                    

if __name__ == '__main__':
    unittest.main()
    