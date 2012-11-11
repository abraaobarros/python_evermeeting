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

class AllMeetings(BaseHandler):
  def get(self):
    meetingsQuery = db.GqlQuery("SELECT * FROM Meeting ")
    self.response.out.write('''
      <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
      <html>
      <head>
          <script type="text/javascript" src="files/jquery-1.7.2.min.js"></script>
          <script type="text/javascript" src="files/jquery.json-2.3.min.js"></script>
        <link href="files/datepicker/css/datepicker.css" rel="stylesheet">
          <link href="css/bootstrap.min.css" rel="stylesheet">
        <script type="text/javascript" src="files/datepicker/js/bootstrap-datepicker.js"></script>
          
        
        <link href="css/style.css" rel="stylesheet">
          
          <title>Criar Reuniao</title>
          <script type="text/javascript"> window.onload = function() {         
            function goToRoom(name){
              if ( $("#username").val() == "") {
                $("#username").parents("div.control-group").addClass("error");
                alert("Please choose an username!");
                return;
              }
              var username = $("#username").val() + "(" + (Math.random() * 100).toFixed(0) + ")";
              window.location = "/chatroom?name=" + name + "&username=" + username;
            } 

            function getRooms(){
              $("#rooms").html("...");
              $.ajax({
              url: "/getrooms",
              success : function(data) { 
                          dados = $.parseJSON(data);
                          var html = "";
                          for (var i = 0; i < dados.length; i++) {
                            html += "<button onclick=\"javascript:goToRoom(\'" + dados[i].name + "\')\" class=\"btn btn-default\"> " + dados[i].name + "</button> ";
                          }
                          $("#rooms").html(html);
                        },
              });
            }
           }

            function goToLink(address) {
              window.location = address;
            }
          function addTopic(){
          $('#lista_topicos').append('<br/><input type="text" id="topic" name="topics[]" placeholder="Adicione um novo topico">' );
          }
          function addEmail(){
          $('#lista_convidados').append('<br/><input type="text" id="email" name="email[]" placeholder="Adicione o email do convidado"> ' );
          }

          </script>
      </head>
      <body style="padding:10px">
        <div class="navbar">
             <div class="navbar-inner">
              <a class="brand" href="#"><img alt="" src="layout/netSaleLogo.png" /></a>
              <ul class="nav">
                <li class="active"><a href="#">Home</a></li>
              </ul>
              <ul class="nav pull-right">
                <li><a href="#">Login</a></li>
              </ul>
              </div>
        </div>

        <div class="row-fluid" style="width:80%;margin-left:auto;margin-right:auto">
           <div class="span12">  ''')

    for meeting in meetingsQuery:
      note = myGetUserNoteStore().getNote(authToken,
                   meeting.noteGuid,
                   True,
                   False,
                   False,
                   False)
      self.response.out.write('''
            <div class="meet">
              <div class="img-rounded meet_title">
                <h5>'''+note.title+'''</h5>
                <small>'''+meeting.horario+' - ' + meeting.data + ''' </small>
              </div>
            </div>''')

    self.response.out.write('''      
        </div>  
      </div>
      
    </div>
       <script src="js/bootstrap.js"></script>
    </body>
    </html>''')