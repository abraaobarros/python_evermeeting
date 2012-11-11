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

# From evernote API
import sys
import hashlib
import binascii
import time
import thrift.protocol.TBinaryProtocol as TBinaryProtocol
import thrift.transport.THttpClient as THttpClient
import evernote.edam.userstore.UserStore as UserStore
import evernote.edam.userstore.constants as UserStoreConstants
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
import evernote.edam.error.ttypes as Errors

#Models

class Meeting(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    #updated = db.DateTimeProperty(auto_now=True)    
    # name = db.StringProperty(required=False)
    # lat = db.StringProperty(required=False)
    # lon = db.StringProperty(required=False)
    data = db.StringProperty(required=False)
    horario = db.StringProperty(required=False)
    noteGuid = db.StringProperty(required=False)

# Real applications authenticate with Evernote using OAuth, but for the
# purpose of exploring the API, you can get a developer token that allows
# you to access your own Evernote account. To get a developer token, visit 
# https://sandbox.evernote.com/api/DeveloperToken.action
authToken = "S=s1:U=3b49c:E=14243ea700d:C=13aec39440d:P=1cd:A=en-devtoken:H=b684971c15b0f5c40e1bdad3b91cb5a3"

def myGetUserNoteStore():
  if authToken == "your developer token":
      print "Please fill in your developer token"
      print "To get a developer token, visit https://sandbox.evernote.com/api/DeveloperToken.action"
      exit(1)

  # Initial development is performed on our sandbox server. To use the production 
  # service, change "sandbox.evernote.com" to "www.evernote.com" and replace your
  # developer token above with a token from 
  # https://www.evernote.com/api/DeveloperToken.action
  evernoteHost = "sandbox.evernote.com"
  userStoreUri = "https://" + evernoteHost + "/edam/user"

  userStoreHttpClient = THttpClient.THttpClient(userStoreUri)
  userStoreProtocol = TBinaryProtocol.TBinaryProtocol(userStoreHttpClient)
  userStore = UserStore.Client(userStoreProtocol)

  versionOK = userStore.checkVersion("Evernote EDAMTest (Python)",
                                     UserStoreConstants.EDAM_VERSION_MAJOR,
                                     UserStoreConstants.EDAM_VERSION_MINOR)
  if not versionOK:
      print "Is my Evernote API version up to date? ", str(versionOK)
      print ""
      exit(1)

  # Get the URL used to interact with the contents of the user's account
  # When your application authenticates using OAuth, the NoteStore URL will
  # be returned along with the auth token in the final OAuth request.
  # In that case, you don't need to make this call.
  noteStoreUrl = userStore.getNoteStoreUrl(authToken)

  noteStoreHttpClient = THttpClient.THttpClient(noteStoreUrl)
  noteStoreProtocol = TBinaryProtocol.TBinaryProtocol(noteStoreHttpClient)
  return NoteStore.Client(noteStoreProtocol)

class BaseHandler(webapp2.RequestHandler):
  def teste(self):
    return 0;