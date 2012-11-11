import webapp2

import os
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import base64
import cgi
import Cookie
import email.utils
import hashlib
import hmac
import logging
import os.path
import time
import urllib
import wsgiref.handlers

from util import *

class GetNotebooks(BaseHandler): 
  def get(self):
    noteStore = myGetUserNoteStore()

    # List all of the notebooks in the user's account        
    notebooks = noteStore.listNotebooks(authToken)
    print "Found ", len(notebooks), " notebooks:"
    for notebook in notebooks:
        print "  * ", notebook.name