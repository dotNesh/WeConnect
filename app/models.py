from werkzeug.security import generate_password_hash
import json

class User:

    #Class Variables
    user_id = 0
    users = {}

    def __init__(self, email, username, password):
        #Class Constructor
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def create_user(self):
        #Every call to this call updates the users dictionary
        #users dictionary has a key user_id whose value is a dictionay with user attributes
        User.user_id += 1
        self.users.update({
            self.user_id:{
            'email':self.email,
            'username':self.username,
            'password':self.password
            }
        })
        
        return self.users
    
    def login(self, email, password):
        self.email = email
        self.password = password
        
class Business:

     #Class Variables
     business_id = 0
     business = {}

     def __init__(self,business_name,category,location,description,username):
         self.business_name = business_name
         self.category = category
         self.location = location
         self.description = description
         self.username = username

     def register_business(self):

         Business.business_id += 1
         self.business.update({
             self.business_id:{
                 'user_id': User.user_id,
                 'business_name': self.business_name,
                 'category':self.category,
                 'location':self.location,
                 'description':self.description,
                 'owner':self.username
             }
         })    

         return self.business
     
     @staticmethod
     def get_all_businesses():
        businesses = Business.business
        if len(businesses) > 0:
            return businesses
        else:
            return {"message":"No businesses.Please add one"}

     @staticmethod
     def delete_business(business_id):
        biz = Business.business
        for key in biz:
            if key == business_id:
                del biz[key]
                return {"message": "Deleted Successfully"}         
           

     @staticmethod   
     def get_business(business_id):
         biz = Business.business
         for key in biz:
                if key == business_id:
                    return biz[key] 

     @staticmethod         
     def update_business(business_id, data):
         biz = Business.business
         for key in biz:
             if key == business_id:
                 if 'category' in data.keys():
                    biz[key]['category'] = data['category']
                 if 'business_name' in data.keys():
                    biz[key]['business_name'] = data['business_name']
                 if 'location' in data.keys():
                     biz[key]['location'] = data['location']
                 if 'description' in data.keys():
                     biz[key]['description'] = data['location']

                 return biz            


     
             

class Reviews:
    # Class variables
    review_id = 0
    reviews = {}

    def __init__(self,title,description):
        self.title = title
        self.description = description

    def add_reviews(self):
        Reviews.review_id += 1
        self.reviews.update({
            self.review_id : {
                'user_id': User.user_id,
                'business_id':Business.business_id,
                'title':self.title,
                'description':self.description
            }
        })           
        return  self.reviews

    @staticmethod
    def get_all_reviews():
        reviews = Reviews.reviews
        if len(reviews) > 0:
            return reviews
        else:
            return {"message":"No Reviews for this business.Please add one"}
    