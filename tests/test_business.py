'''WeConnect Business Test File'''
import unittest
import json
from app import app

class BusinessendpointsTestCase(unittest.TestCase):
    '''Business Class Tests'''
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

    def test_add_business(self):
        '''Test business registration'''
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(self.dict),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Business Successfully Registered")
    def test_if_no_token_passed(self):
        '''Test business registration if no token'''
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(self.dict),
                                 headers={
                                     "Content-Type": "application/json"
                                     })
        self.assertEqual(response.status_code, 401)
    def test_business_name_empty(self):
        '''Test for blank business name'''
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(dict(business_name="", category="software",
                                                      location="Nairobi",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['business_name-Error:']["message"], "business_name cannot be an empty string")

    def test_category_empty(self):
        '''Test for blank category'''
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="",
                                                      location="Nairobi",
                                                      description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['category-Error:']["message"], "category cannot be an empty string")

    def test_location_empty(self):
        '''Test for blank location'''
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",
                                                      location="", description="This is Andela")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['location-Error:']["message"], "location cannot be an empty string")

    def test_description_empty(self):
        '''Test for blank description'''
        response = self.app.post("/api/v1/businesses",
                                 data=json.dumps(dict(business_name="Andela", category="software",
                                                      location="Nairobi", description="")),
                                 headers={
                                     "Authorization": "Bearer {}".format(self.access_token),
                                     "Content-Type": "application/json"
                                     })

        self.assertEqual(response.status_code, 406)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg['description-Error:']["message"], "description cannot be an empty string")
    def test_get_businesses(self):
        '''test get all businesses'''
        response = self.app.get("/api/v1/businesses",
                                headers={
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 200)
    def test_get_business(self):
        '''test get one business'''
        response = self.app.get("/api/v1/businesses/1")
        self.assertEqual(response.status_code, 200)
    def test_delete_business(self):
        '''Test Business Delete'''
        response = self.app.delete("/api/v1/businesses/2",
                                   headers={
                                       "Authorization": "Bearer {}".format(self.access_token),
                                       "Content-Type": "application/json"
                                       })
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Deleted Successfully")
    def test_delete_business_not_owner(self):
        '''Test only owner can delete a business'''
        response = self.app.delete("/api/v1/businesses/1",
                                   headers={
                                       "Authorization": "Bearer {}".format(self.access_token2),
                                       "Content-Type": "application/json"
                                       })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "You cannot delete a business that is not yours")
    def test_delete_business_not_found(self):
        '''test not found'''
        response = self.app.delete("/api/v1/businesses/11",
                                   headers={
                                       "Authorization": "Bearer {}".format(self.access_token),
                                       "Content-Type": "application/json"
                                       })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Cannot Delete. Resourse Not Found")
    def test_update_business(self):
        '''Test for update a business'''
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(dict(category="software dev", location="lagos")),
                                headers={
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Successfully Updated")
    def test_update_business_not_owner(self):
        '''Test only owner can update'''
        response = self.app.put("/api/v1/businesses/1",
                                data=json.dumps(dict(category="software dev", location="lagos")),
                                headers={
                                    "Authorization": "Bearer {}".format(self.access_token2),
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "You cannot update a business that is not yours")
    def test_update_business_not_found(self):
        '''Test no business'''
        response = self.app.put("/api/v1/businesses/11",
                                data=json.dumps(dict(category="software dev", location="lagos")),
                                headers={
                                    "Authorization": "Bearer {}".format(self.access_token),
                                    "Content-Type": "application/json"
                                    })
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual(response_msg["message"], "Cannot Update. Resource Not Found")


if __name__ == '__main__':
    unittest.main()        