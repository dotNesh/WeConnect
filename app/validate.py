'''File containing input validations'''
import re


def empty(data):
    '''method to validate username input'''
    newname = re.sub(r'\s+', '', data)
    namelength = len(newname)
    if namelength == 0:
        return True
