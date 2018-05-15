'''WeConnect Users Test File'''
import unittest
import json
from app import app
class UserendpointsTestcase(unittest.TestCase):
    '''User endpoints test class'''
    def setUp(self):
        self.app = app.test_client(self)
        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="kmunene@live.com", username="kelvin",
                                           password="12345678")), content_type="application/json")

        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="ed@live.com", username="ed",
                                           password="12345678")), content_type="application/json")
        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="mwendarooney@gmail.com", username="dee",
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
                                 data=json.dumps(dict(email="nina@live.com", username="nina",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "User Succesfully Registered")
    
    def test_password_length(self):
        '''Test password length'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="mutha@live.com", username="mutha",
                                                      password="123456")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Password is weak! Must have atleast 8 characters")

    def test_email_not_empty(self):
        '''Test for blank email input'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="", username="nina",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['email-Error:']['message'], "email cannot be an empty string")
    
    def test_email_pattern(self):
        '''Test email pattern'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="jeff@gmail", username="jeff",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['message'], "Email format is user@example.com")

    def test_username_not_empty(self):
        '''Test for blank username input'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="nina@live.com", username="",
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
                                 data=json.dumps(dict(email="nina@live.com", username="ni na",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Username cannot contain white spaces")

    def test_email_already_registered(self):
        '''Test for existing email'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="mwendarooney@gmail.com", username="kelin",
                                                      password="12345678")),
                                 content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Email already existing.")

    def test_username_exists(self):
        '''test for existing username'''
        response = self.app.post("/api/v1/auth/register",
                                 data=json.dumps(dict(email="kev@live.com", username="kelvin",
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


    def test_change_missing_old_password(self):
        '''Test for missing old password'''
        response = self.app.post("/api/v1/auth/change-password",
                                 data=json.dumps(dict(new_password="12345667")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['old_password-Error:']["message"],
                         "old_password cannot be missing")

    def test_change_missing_new_password(self):
        '''Test for missing new password'''
        response = self.app.post("/api/v1/auth/change-password",
                                 data=json.dumps(dict(old_password="12345667")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['new_password-Error:']["message"],
                         "new_password cannot be missing")
    def test_password_change(self):
        '''Test for password change'''
        access_token = json.loads(self.user.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/change-password",
                                 data=json.dumps(dict(old_password="12345678",
                                                      new_password="12348765")),
                                 headers={
                                     "Authorization": "Bearer {}".format(access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Reset successful")

    def test_password_change_length(self):
        '''Test for password length in password'''
        user = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="dee", password="12348765")),
                                 content_type="application/json")

        access_token = json.loads(user.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/change-password",
                                 data=json.dumps(dict(old_password="12348765",
                                                      new_password="123487")),
                                 headers={
                                     "Authorization": "Bearer {}".format(access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Password is weak! Must have atleast 8 characters")
    
    
    def test_login_after_password_change(self):
        '''Test for login after change'''
        access_token = json.loads(self.user2.data.decode())['access_token']

        self.app.post("/api/v1/auth/change-password",
                      data=json.dumps(dict(old_password="12345678",
                                           new_password="12348765")),
                      headers={
                          "Authorization": "Bearer {}".format(access_token),
                          "Content-Type": "application/json"
                          })

        response = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="dee", password="12348765")),
                                 content_type="application/json")
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "You are logged in successfully")
    def test_wrong_password_change(self):
        '''Test for wrong old password in change'''
        user = self.app.post("/api/v1/auth/login",
                                 data=json.dumps(dict(username="ed", password="12348765")),
                                 content_type="application/json")

        access_token = json.loads(user.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/change-password",
                                 data=json.dumps(dict(old_password="12345667",
                                                      new_password="12345!@0")),
                                 headers={
                                     "Authorization": "Bearer {}".format(access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],
                         "Wrong Password. Cannot reset. Forgotten password?")    

    def test_password_reset(self):
        '''Test for password reset'''
        response = self.app.post("/api/v1/auth/reset-password",
                                  data=json.dumps(dict(username="dee")),
                                  headers ={
                                      "Content-Type": "application/json"   
                                  })
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],
                         "An email has been sent with your new password!")
    
    def test_password_reset_no_user(self):
        '''Test for reset if no existing user'''
        response = self.app.post("/api/v1/auth/reset-password",
                                  data=json.dumps(dict(username="deelo")),
                                  headers ={
                                      "Content-Type": "application/json"   
                                  })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],
                         "Non-existent user. Try signing up")
    
    def test_logout(self):
        '''Test user logout'''
        response = self.app.post("/api/v1/auth/logout",
                                headers ={
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code,200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],
                         "Logout successful")
    
    def test_activity_after_loguout(self):
        '''Test if token is blacklisted'''
        self.app.post("/api/v1/auth/logout",
                                headers ={
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        response = self.app.post("/api/v1/businesses",
                      data=json.dumps(dict(business_name="Waridi", category="food",
                                           location="Kisumu", description="Sweet")),
                      headers={
                          "Authorization": "Bearer {}".format(self.access_token),
                          "Content-Type": "application/json"
                          })
        
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["msg"],
                         "Token has been revoked")

if __name__ == '__main__':
    unittest.main()
    