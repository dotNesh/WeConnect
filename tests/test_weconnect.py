import unittest
from app.models import User, Business, Reviews

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

if __name__ == '__main__':
    unittest.main()        
        

