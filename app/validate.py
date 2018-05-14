'''File containing input validations'''
import re

def empty(**data):
    '''method to validate username input'''
    messages = {}
    for key in data:
        newname = re.sub(r'\s+', '', data[key])
        if not newname:
            message = {'message': key + ' cannot be an empty string'}
            messages.update({key+'-Error:':message})
    return messages
def whitespace(data):
    '''method to validate white'''
    newname = re.sub(r'\s+', '', data)
    afterlength = len(newname)
    actuallength = len(data)
    if afterlength != actuallength:
        return True
def val_none(**data):
    '''method to check none'''
    messages = {}
    for key in data:
        if data[key] is None:
            message = {'message': key + ' cannot be missing'}
            messages.update({key+'-Error:':message})
    return messages

def pass_length(data):
    if len(data) < 8:
        return True   
