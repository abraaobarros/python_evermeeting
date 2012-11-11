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

# /createmeeting?title=ReuniaoUrgente&goal=AjeitarTudo
class CreateMeeting(BaseHandler): 
  def get(self):
    newNote = Note()
    newNote.title = self.request.get('title')
    # newNote.content += self.request.get('date')
    newNote.content += self.request.get('goal')
    # newNote.content += self.request.get('schedule')
    # newNote.content += self.request.get('duration')
    # newNote.content += self.request.get('place')
    # newNote.content += self.request.get('topics')
    # newNote.content += self.request.get('invites')
    # newNote.content += self.request.get('responsabilities')
    guid = myGetUserNoteStore().createNote(authToken, newNote)
    newMeeting = Meeting(guid)
    newMeeting.put()
    print guid