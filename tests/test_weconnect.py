#WeConnect Test File
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
                
    def test_user_register(self):
        '''Test User Registration method'''
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="nina@live", username="nina",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"User Succesfully Registered")

    def test_email_not_empty(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="",username="nina",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"email cannot be an empty string")

    def test_username_not_empty(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="nina@live",username="",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"username cannot be an empty string") 

    def test_password_not_empty(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="nina@live.com",username="nina",
                                password="")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"password cannot be an empty string")       


    def test_email_already_registered(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kelvin@live",username="kelin",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Email already existing.")

    def test_username_already_registered(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kev@live",username="kelvin",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Username already existing.")
    def test_user_login_empty_username(self):
        response = self.app.post("/api/v1/auth/login",
                    data=json.dumps(dict(username="",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"username cannot be an empty string")
    def test_user_login_empty_password(self):
        response = self.app.post("/api/v1/auth/login",
                    data=json.dumps(dict(username="kelvin",
                                password="")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"password cannot be an empty string")    
    def test_user_login(self):
        response = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="kelvin",password="12345678")),
                                         content_type="application/json")

        #self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You are logged in successfully")
        self.assertTrue(response_msg['access_token'])

    def test_wrong_password(self):
        response = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="kelvin",password="123678")),
                                         content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Wrong password") 

    def test_non_existing_user(self):
        response = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="melvin",password="12345678")),
                                         content_type="application/json")
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Non-existent user. Try signing up")

    def test_password_reset(self):
        self.login_user2 = self.app.post("/api/v1/auth/login",
                    data=json.dumps(dict(username="ed", 
                        password="12345678")),content_type="application/json")                        

        self.access_token2 = json.loads(self.login_user2.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/reset-password",
                        data=json.dumps(dict(old_password="12345678",new_password="12345")),
                                        headers = {
                                                "Authorization": "Bearer {}".format(self.access_token2),
                                                "Content-Type": "application/json"
                                })                                     
        #self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Reset successful")

    def test_password_reset_wrong_old_password(self):
        self.login_user2 = self.app.post("/api/v1/auth/login",
                    data=json.dumps(dict(username="ed", 
                        password="12345")),content_type="application/json")                        

        self.access_token2 = json.loads(self.login_user2.data.decode())['access_token']

        response = self.app.post("/api/v1/auth/reset-password",
                        data=json.dumps(dict(old_password="12345667",new_password="12345!@")),
                                        headers = {
                                                "Authorization": "Bearer {}".format(self.access_token2),
                                                "Content-Type": "application/json"
                                })                                     
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Wrong Password. Cannot reset. Forgotten password?")    
        

class BusinessendpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)
        #User 1
        self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kelvin@live",username="kelvin",
                                password="12345678")), content_type="application/json")

        
        self.login_user = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="kelvin",password="12345678")),
                                         content_type="application/json")                
      
        self.access_token = json.loads(self.login_user.data.decode())['access_token']

        #User 2
        self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="lynn@live",username="lynn",
                                password="12345678")), content_type="application/json")

        
        self.login_user2 = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="lynn",password="12345678")),
                                         content_type="application/json")                
      
        self.access_token2 = json.loads(self.login_user2.data.decode())['access_token']

        #Business 1
        self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="Mutura",
                                    category="food",
                                    location="Kisumu",
                                    description="Sweet")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.dict = dict(
                    business_name="Andela",
                    category="software",
                    location="Nairobi",
                    description="This is Andela")

    def test_add_business(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(self.dict),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
                       


        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Business Successfully Registered") 

    def test_unauthorized_if_no_token_passed(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps( self.dict),
                                headers = {
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401)
      

    def test_business_name_empty(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="",
                                    category="software",
                                    location="Nairobi",
                                    description="This is Andela")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"business_name cannot be an empty string")

    def test_category_empty(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="",
                                    location="Nairobi",
                                    description="This is Andela")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"category cannot be an empty string")

    def test_location_empty(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="software",
                                    location="",
                                    description="This is Andela")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"location cannot be an empty string")

    def test_description_empty(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="software",
                                    location="Nairobi",
                                    description="")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"description cannot be an empty string")
    
    


    def test_get_businesses(self):
         response = self.app.get("/api/v1/businesses",
                                    headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
         self.assertEqual(response.status_code, 200)   

    def test_get_business(self):

        response = self.app.get("/api/v1/businesses/1")
        
        self.assertEqual(response.status_code, 200)         
    def test_delete_business(self):
            
            response = self.app.delete("/api/v1/businesses/2",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })  

            self.assertEqual(response.status_code, 200)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertEqual(response_msg["message"],"Deleted Successfully") 
    def test_delete_business_not_owner(self):
            
            response = self.app.delete("/api/v1/businesses/1",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                })  

            self.assertEqual(response.status_code, 401)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertEqual(response_msg["message"],"You cannot delete a business that is not yours")
    def test_delete_business_not_found(self):
        '''test not found'''           
        response = self.app.delete("/api/v1/businesses/11",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })  

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Delete. Resourse Not Found")   
    def test_update_business(self):
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(dict(
                                    category="software development",
                                    location="lagos",)
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 201) 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Successfully Updated") 
    def test_update_business_not_owner(self):
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(dict(
                                    category="software development",
                                    location="lagos",)
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 401) 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"You cannot update a business that is not yours")                          
    def test_update_business_not_found(self):
        '''Test no business'''
        response = self.app.put("/api/v1/businesses/11",
                                data=json.dumps(dict(
                                    category="software development",
                                    location="lagos",)
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
        self.assertEqual(response.status_code, 404) 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Cannot Update. Resource Not Found") 

class ReviewendpointsTestCase(unittest.TestCase):
    '''Reviews test class'''
    def setUp(self):
        self.app = app.test_client(self)

        self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kelvin@live",username="kelvin",
                                password="12345678")), content_type="application/json")

        
        self.login_user = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="kelvin",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token = json.loads(self.login_user.data.decode())['access_token']       
    
    def test_add_review(self):
        '''test add review'''
        response = self.app.post("/api/v1/businesses/2/reviews",
                                data=json.dumps(dict(
                                    title="Andela",
                                    description="This is Andela")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 201)     

    def test_get_reviews(self):
        response = self.app.get("/api/v1/businesses/2/reviews",
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })

        self.assertEqual(response.status_code, 200)                        


if __name__ == '__main__':
    unittest.main()
    


        

