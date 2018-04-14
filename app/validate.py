#File containing input validations
import re
from flask import jsonify


def empty(data):
    '''method to validate username input'''
    newname = re.sub(r'\s+', '',data) 
    namelength = len(newname)
    if namelength == 0:
        return True