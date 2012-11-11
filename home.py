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

import json
_parse_json = json.loads

# our stuff
from util import *
from getnotebooks import *
from createmeetings import *

class Meeting(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    #updated = db.DateTimeProperty(auto_now=True)    
    # name = db.StringProperty(required=False)
    # lat = db.StringProperty(required=False)
    # lon = db.StringProperty(required=False)
    # currentnumber = db.IntegerProperty(required=False)
    noteGuid = db.StringProperty(required=False)
    
class Message(db.Model):
    created = db.DateTimeProperty(auto_now_add=True)
    room = db.StringProperty(required=False)
    user = db.StringProperty(required=False)
    type = db.StringProperty(required=False)
    number = db.IntegerProperty(required=False)
    messagetext = db.StringProperty(required=False)
    votetarget = db.StringProperty(required=False)
    votetype = db.StringProperty(required=False)
  
class Home(BaseHandler):
  def get(self):
    template_values = { }
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    rendered = template.render(path, template_values)
    self.response.out.write(rendered)
    
class GetRooms(BaseHandler):
  def get(self):
    roomsQuery = db.GqlQuery("SELECT * FROM Room ")
    result = []
    for room in roomsQuery:
      r = { }
      r['name'] = room.name;
      r['lat'] = room.lat
      r['lon'] = room.lon
      result.append(r)
    self.response.out.write(json.dumps(result))
    
class NewRoom(BaseHandler):
  def get(self):
    template_values = { }
    path = os.path.join(os.path.dirname(__file__), 'newroom.html')
    rendered = template.render(path, template_values)
    self.response.out.write(rendered)
    
class ChatRoom(BaseHandler):
  def get(self):
    name = self.request.get('name')
    username = self.request.get('username')
    roomQuery = db.GqlQuery("SELECT * "
                            "FROM Room "
                            "WHERE name = :1 ",
                            name )
    exists = False
    for r in roomQuery:
      exists = True
    if exists == False:
      self.response.out.write("There is no room with this name: " + name)
      return
  
    template_values = { 'roomname' : name, 
                        'username' : username }
    path = os.path.join(os.path.dirname(__file__), 'chatroom.html')
    rendered = template.render(path, template_values)
    self.response.out.write(rendered)

class CreateRoom(BaseHandler): 
  def post(self):
    name = self.request.get('name')
    roomQuery = db.GqlQuery("SELECT * "
                            "FROM Room "
                            "WHERE name = :1 ",
                            name )
    exists = False
    for r in roomQuery:
      exists = True
    if exists == True:
      self.response.out.write("nameexists")
      return
    
    lat = self.request.get('lat')
    lon = self.request.get('lon')
    newRoom = Room(name = name,
                   lat = lat,
                   lon = lon,
                   currentnumber = 0)
    newRoom.put()
    self.response.out.write("success")

    
class CreateMessage(BaseHandler): 
  def post(self):
    logging.getLogger('bla').info('room: ' + self.request.get('room') + ", user: " + self.request.get('user') + ", data: " + self.request.get('data'));
  
    room = self.request.get('room')
    roomQuery = db.GqlQuery("SELECT * "
                            "FROM Room "
                            "WHERE name = :1 ",
                            room )
    
    user = self.request.get('user')
    type = self.request.get('type')
    votetype = ""
    if type == "v":
      votetarget = self.request.get('votetarget')
      logging.info("votetarget: "+votetarget)
      votetype = self.request.get('votetype')
      voteQuery = db.GqlQuery("SELECT * "
                              "FROM Message "
                              "WHERE room = :1 AND votetarget = :2 AND user = :3",
                              room, votetarget, user)
      voteexists = False;
      for v in voteQuery:
        voteexists = True;
      if voteexists == True:
        self.response.out.write(str(-1));
        return
    
    number = 0;
    for r in roomQuery:
      number = r.currentnumber;
      r.currentnumber = number + 1
      r.put()
    
    
    messagetext = ""
    if type == "m":
      messagetext = self.request.get('messagetext')
      votetarget = "0" 

    newMessage = Message(room = room,
                         number = number,
                         user = user,
                         type = type,
                         messagetext = messagetext,
                         votetarget = votetarget,
                         votetype = votetype)
    newMessage.put()
    self.response.out.write(str(number));
    
class RecoverMessages(BaseHandler): 
  def post(self):
    room = self.request.get('room')
    roomQuery = db.GqlQuery("SELECT * "
                            "FROM Room "
                            "WHERE name = :1 ",
                            room )
    number = 0;
    for r in roomQuery:
      number = r.currentnumber;
    
    all = self.request.get('all')
    logging.info("recover all: "+all)
    missing = []
    if all == "true":
      for i in range(0, number):
        missing.append(i)
    else:
      missing = json.loads(self.request.get('missing'))
    
    result = []
    for i in missing:
      if i < number:
        messageQuery = db.GqlQuery("SELECT * "
                                   "FROM Message "
                                   "WHERE room = :1 AND number = :2",
                                   room, i)
        for message in messageQuery:
          m = { }
          m['type'] = message.type
          m['user'] = message.user
          m['number'] = message.number
          m['messagetext'] = message.messagetext
          m['votetarget'] = message.votetarget
          m['votetype'] = message.votetype
          result.append(m)
    self.response.out.write(json.dumps(result))

app = webapp2.WSGIApplication([
    ('/', Home), 
    ('/getnotebooks', GetNotebooks),
    ('/createmeeting', CreateMeeting )
    # ('/createroom', CreateRoom),
    # ('/getrooms', GetRooms),
    # ('/home', Home),
    # ('/newroom', NewRoom),
    # ('/createmessage', CreateMessage),
    # ('/recovermessages', RecoverMessages),
    # ('/chatroom', ChatRoom),

    ],
  debug=True)