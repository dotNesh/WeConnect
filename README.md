[![Build Status](https://travis-ci.org/kmunene/WeConnect.svg?branch=challenge2)](https://travis-ci.org/kmunene/WeConnect)
[![Coverage Status](https://coveralls.io/repos/github/kmunene/WeConnect/badge.svg?branch=challenge2)](https://coveralls.io/github/kmunene/WeConnect?branch=challenge2)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b153ab4d8eba430fa27d8047b3a7f97c)](https://www.codacy.com/app/kmunene/WeConnect?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=kmunene/WeConnect&amp;utm_campaign=Badge_Grade)

## WeConnect

This is an API for WeConnect, a platform that brings businesses and individuals together. This platform creates awareness for businesses and gives the users the ability to:

- Register an account and Login into it.
- Register, Update and delete a Business .
- View all Businesses.
- View One Business.
- Post Reviews to a business.
- View all Reviews to a business
- Change and Reset a users password

## Prerequisites

- Python 3.6 or a later version

## Installation
Clone the repo.
```
$ git clone https://github.com/kmunene/WeConnect.git
```
and cd into the folder:
```
$ /WeConnect
```
## Virtual environment
Create a virtual environment:
```
python3 -m venv venv
```
Activate the environment
```
$ source venv/bin/activate
```
## Dependencies
Install package requirements to your environment.
```
pip install -r requirements.txt
```

## Testing
To set up unit testing environment:

```
$ pip install nose
$ pip install coverage
```

To run tests perform the following:

```
$ nosetests --with-coverage
```

## Start The Server
To start the server run the following command
```
python run.py
```
The server will run on port: 5000

## Testing API on Postman

*Note* Ensure that after you succesfully login a user, you use the generated token in the authorization header for the endpoints that require authentication. Remeber to add Bearer before the token as shown:
```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9eyJpYXQiO 
```


### API endpoints

| Endpoint | Method |  Functionality | Authentication |
| --- | --- | --- | --- |
| /api/auth/v1/register | POST | Creates a user account | FALSE
| /api/auth/v1/login | POST | Logs in a user | TRUE
| /api/auth/v1/logout | POST | Logs out a user | TRUE
| /api/auth/v1/reset-password | POST | Reset user password | TRUE
| /api/auth/v1/change-password | POST | Change user password | TRUE
| /api/v1/businesses | POST | Register a business | TRUE
| /api/v1/businesses | GET | Retrieves all businesses | FALSE 
| /api/v1/businesses/{businessid} | GET | Get a business | FALSE
| /api/v1/businesses/{businessid} | PUT | Update a business profile | TRUE
| /api/v1/businesses/{businessid} | DELETE | Delete a business | TRUE
| /api/v1/businesses/{businessid}/reviews | POST | Post a review on a business | TRUE
| /api/v1/businesses/{businessid}/reviews | GET | Get all reviews to a business | FALSE



## API Documentation

## Authors

* **Kariuki Kelvin** - [kmunene](https://github.com/kmunene)

## Acknowledgments
* Flevian Kanaiza
* **Stephen Muthama** - [muthash](https://github.com/muthash)
* Linnette Wanjiru

 
