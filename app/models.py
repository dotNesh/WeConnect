from werkzeug.security import generate_password_hash

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

        
class Business:

    #Class Variables
     business_id = 0
     business = {}

     def __init__(self,business_name,category,location,description):
         self.business_name = business_name
         self.category = category
         self.location = location
         self.description = description

     def register_business(self):

         Business.business_id += 1
         self.business.update({
             self.business_id:{
                 'user_id': User.user_id,
                 'business_name': self.business_name,
                 'category':self.category,
                 'location':self.location,
                 'description':self.description,
             }
         })    

         return self.business

     
     @staticmethod
     def get_all_businesses():
        return Business.business    

class Reviews:
    #Class variables
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


         

