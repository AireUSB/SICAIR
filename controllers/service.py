# -*- coding: utf-8 -*-

def index(): 
    if auth.has_membership('air'):
        redirect('hours')
    message = T("Hello world")
    return locals()

def hours():
    pass
