import unittest
import json
from app.models import User, Business, Reviews
from app import app

class UserTestcase(unittest.TestCase):
    def setUp(self):
        User.users = {}
        self.person = User("kmunene@live.com","Kelvin","12345")
       

    def test_create_user(self):
        #Test before person is created
        self.assertEqual(len(self.person.users),0)
        self.assertEqual(self.person.user_id,0)
        
        #After person is created
        self.person.create_user()
        self.assertIsInstance(self.person, User)
        self.assertEqual(len(self.person.users),1)
        self.assertEqual(self.person.user_id,1) #Test if user_id works += 1
        

    def tearDown(self):
        del self.person    

class BusinessTestcase(unittest.TestCase):
    def setUp(self):
        Business.business = {}
        self.bizna = Business("Mutura kwa Maiko", "Restaurant","Kiamaiko","Best Mutura in town")

    def test_register_business(self):
        #Before registering a business
        self.assertEqual(len(self.bizna.business),0)
        self.assertEqual(self.bizna.business_id,0) 

        #After registering a business   
        self.bizna.register_business()
        self.assertIsInstance(self.bizna, Business)
        self.assertEqual(len(self.bizna.business),1)
        self.assertEqual(self.bizna.business_id, 1)

    def tearDown(self):
        del self.bizna   

class ReivewsTestcase(unittest.TestCase):
    def setUp(self):   
        Reviews.reviews = {}
        self.post = Reviews("Very Tasy","I really liked the place, its clean, nice ambience, great music") 

    def test_add_reviews(self):
        #Before posting a review
        self.assertEqual(len(self.post.reviews),0)
        self.assertEqual(self.post.review_id,0)  

        #After posting a review
        self.post.add_reviews()
        self.assertIsInstance(self.post, Reviews)  
        self.assertEqual(len(self.post.reviews),1)
        self.assertEqual(self.post.review_id,1)  

class UserendpointsTestcase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client(self)
        self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kelvin@live",username="kelvin",
                                password="12345678")), content_type="application/json")
      

    def test_user_register(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="nina@live",username="nina",
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
        self.assertEqual(response_msg["message"],"Email should not be an empty string")

    def test_username_not_empty(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="nina@live",username="",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Username should not be an empty string") 

    def test_password_not_empty(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="nina@live.com",username="nina",
                                password="")), content_type="application/json")

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Password should not be an empty string")       


    def test_already_registered(self):
        response = self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kelvin@live",username="kelvin",
                                password="12345678")), content_type="application/json")

        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Account is already existing.")
        
    def test_user_login(self):
        response = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="kelvin",password="12345678")),
                                         content_type="application/json")

        self.assertEqual(response.status_code, 200)
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

class BusinessendpointsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client(self)

        self.app.post("/api/v1/auth/register",
                    data=json.dumps(dict(email="kelvin@live",username="kelvin",
                                password="12345678")), content_type="application/json")

        
        self.login_user = self.app.post("/api/v1/auth/login",
                        data=json.dumps(dict(username="kelvin",password="12345678")),
                                         content_type="application/json") 
      
        self.access_token = json.loads(self.login_user.data.decode())['access_token']

    def test_add_business(self):
       

        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="software",
                                    location="Nairobi",
                                    description="This is Andela")
                                ),
                                headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                })
                       


        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"],"Business Successfully Registered") 

    def test_unauthorized_if_no_token_passed(self):
        response = self.app.post("/api/v1/businesses",
                                data=json.dumps(dict(
                                    business_name="Andela",
                                    category="software",
                                    location="Nairobi",
                                    description="This is Andela")
                                ),
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
        self.assertEqual(response_msg["message"],"Business name should not be an empty string")

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
        self.assertEqual(response_msg["message"],"Category should not be an empty string")

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
        self.assertEqual(response_msg["message"],"Location should not be an empty string")

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
        self.assertEqual(response_msg["message"],"Description should not be an empty string")
    
    


    def test_get_businesses(self):
         response = self.app.get("/api/v1/businesses",
                                    headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
         self.assertEqual(response.status_code, 200)   

    def test_get_business(self):

        response = self.app.get("/api/v1/businesses/1",
                                    headers = {
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)            

if __name__ == '__main__':
    unittest.main()
    


        

