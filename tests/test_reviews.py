'''WeConnect Reviews Test File'''
import unittest
import json
from app import app

class BusinessendpointsTestCase(unittest.TestCase):
    '''Reviews Class Tests'''
    def setUp(self):
        self.app = app.test_client(self)
        #User 1
        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="kelvin@live.com", username="kelvin",
                                           password="12345678")),
                      content_type="application/json")
        self.login_user = self.app.post("/api/v1/auth/login",
                                        data=json.dumps(dict(username="kelvin",
                                                             password="12345678")),
                                        content_type="application/json")
        self.access_token = json.loads(self.login_user.data.decode())['access_token']

        #User 2
        self.app.post("/api/v1/auth/register",
                      data=json.dumps(dict(email="lynn@live.com", username="lynn",
                                           password="12345678")),
                      content_type="application/json")
        self.login_user2 = self.app.post("/api/v1/auth/login",
                                         data=json.dumps(dict(username="lynn",
                                                              password="12345678")),
                                         content_type="application/json")
        self.access_token2 = json.loads(self.login_user2.data.decode())['access_token']

        #Business 1
        self.app.post("/api/v1/businesses",
                      data=json.dumps(dict(business_name="Mutura", category="food",
                                           location="Kisumu", description="Sweet")),
                      headers={
                          "Authorization": "Bearer {}".format(self.access_token),
                          "Content-Type": "application/json"
                          })

        self.dict = dict(business_name="Andela", category="software", location="Nairobi",
                         description="This is Andela")

    def test_add_review(self):
        '''test add review'''
        response = self.app.post("/api/v1/businesses/2/reviews",
                                 data=json.dumps(dict(title="Andela",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 201)
    def test_get_reviews(self):
        '''Test get all reviews'''
        response = self.app.get("/api/v1/businesses/2/reviews",
                                headers={
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)                         
