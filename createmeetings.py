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

from util import *

# /createmeeting?title=ReuniaoUrgente&goal=AjeitarTudo
class CreateMeeting(BaseHandler): 
  def get(self):
    newNote = Types.Note()
    newNote.title = self.request.get('titulo')
    # newNote.content += self.request.get('date')
    newNote.content = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
    <en-note style="margin:10px;background-color:rgb(0, 0, 0);font-size:17px;color:rgb(0, 0, 0);text-align:center;font-family:Garamond;">
        <div style="font-size:17px;color:rgb(80, 80, 80);text-align:center;font-family:Garamond;x-evernote:food-meal;">
            <div style="max-width:600px;padding-bottom:0.8%;background-color:#fff;box-shadow:0 3px 15px rgba(0,0,0,.5);-webkit-box-shadow:0 3px 15px rgba(0,0,0,.5);margin:20px auto;">
                <div style="margin-left: 4%;text-align:left;">
                    <div style="padding-top:4%;padding-right:4%;">
                        <h1 style="margin-top:30px;margin-bottom:1%;font-size:36px;font-weight:100;color:rgb(25, 75, 150);">
                            <span style="x-evernote:title">''' + self.request.get('titulo') + '''</span>
                        </h1>
                        <hr style="margin:0px;border-top-color:rgb(25, 75, 150);border-top-width:1px;border-top-style:solid;" />
                        <p style="line-height:17px;margin-bottom:0px;font-size:22px;font-weight:bold;">
                          <span style="x-evernote:place-name"> </span> 
                        </p>
                        <p style="line-height:17px;">
                        <span style="x-evernote:meal-review">
                        
                        </span>
                        </p>
                        <p style="line-height:17px;text-align:right;margin-top:0px;font-size:16px;">
                        Nov 10, 2012
                        </p>
                    </div>
                    
                    <div style="padding-top:4%;padding-right:4%;">
                        <p style="text-align:center;padding:8px;background-color:rgb(225, 225, 235); overflow: hidden; text-overflow: ellipsis;">
                            <b style="font-size:20px;">Goal</b>
                            <br style="font-size:18px;"> '''+self.request.get('objetivo')+'''</br>
                        </p>
                    </div>
                    
                    <table style="width:100%;height:auto;padding-left:4%;padding-right:4%;">
                        <tr>
                            <td style="font-size:18px;">
                                <b style="font-size:20px;">Date</b><br/>'''+self.request.get('data')+'''<p/>
                            </td>
                            <td rowspan="3" style="font-size:18px;">
                                <b style="font-size:20px;">Place</b><br/>'''+self.request.get('lugar')+'''<p/>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size:18px;">
                                <b style="font-size:20px;">Schedule</b><br/>'''+self.request.get('horario')+'''<p/>
                            </td>
                        </tr>
                        <tr>
                            <td style="font-size:18px;">
                                <b style="font-size:20px;">Duration</b><br/>'''+self.request.get('duracao')+'''</td>
                        </tr>
                    </table>
                </div>
                <div style="text-align:right;margin:0;padding-right:2%;padding-top:50px;padding-bottom:0px;clear:both;font-size:12px;color:rgb(150, 150, 150);">
                    created with EVERNOTE MEETING
                </div>
            </div>
            
        </div>
    </en-note>'''
    # newNote.content += self.request.get('schedule')
    # newNote.content += self.request.get('duration')
    # newNote.content += self.request.get('place')
    # newNote.content += self.request.get('topics')
    # newNote.content += self.request.get('invites')
    # newNote.content += self.request.get('responsabilities')
    guid = myGetUserNoteStore().createNote(authToken, newNote).guid
    newMeeting = Meeting(noteGuid = guid,
                         data = self.request.get('data'),
                         horario = self.request.get('horario'))
    newMeeting.put()
    self.redirect('/allmeetings')