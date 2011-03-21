#!/usr/bin/env python
#
# Copyright 2011 Hunter Lang
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os.path
import re
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import codecs
import uuid
import base64
import os
import os.path
import random
import sys
import commands
import datetime
import pyPdf
from mmap import mmap

from tornado.options import define, options

define("port", default=8019, help="run on the given port", type=int)

# This defines the applications routes
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
			(r"/", IndexHandler),
			(r"/static", IndexHandler),
			(r"/test", TestHandler),
			(r"/logtest", LogHandler),

			
        ]
        
        #print "Image Server is now running on port 8080...."
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

# Redirects to the Cappuccino app
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		#output_file.write(remoteIP)
		self.redirect("/static/index.html")
		
class LogHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		self.finish("hey")

class TestHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		file_content = self.request.files['file'][0]
		file_body = file_content['body']
		filename = file_content['filename']
		print filename

		output_file = open("docs/" + filename, 'w')
		output_file.write(file_body)
		output_file.close()
		
		
		
		ext = os.path.splitext(filename)[1]
		if ext == ".doc" or ext == ".docx":
			print "It's a doc! It's a doc! -Admiral Ackbar"
			commands.getstatusoutput('textutil -convert txt docs/' + filename)

		elif ext == ".pages":
			os.rename(filename, (os.path.splitext(filename)[0] + ".zip"))
			commands.getstatusoutput('unzip -j ' + filename + ' QuickLook/Preview.pdf')
			pdf = pyPdf.PdfFileReader(open("Preview.pdf", "rb"))
			n = open(os.path.splitext(filename)[0] + ".txt", "w")
			for page in pdf.pages:
				n.write(unicode(page.extractText(), "utf-8", errors="replace"))
			n.close()
		else:
			val = {
				"URL": "That file type is currently unsupported by Document Uploader."
			}
			self.finish(val)
		
		str = os.path.splitext(filename)[0]
		f = open("docs/" + str + ".txt")
		pref = open('prefix.txt')
		prefix = pref.read()
					
		name = "Hunter Lang"
		subject = "English 9 Honors"
		date = "May 14, 2011"
		period = 4
		perstr = "Period " + repr(period)
		title = "This is a jQuery test."
		str = rand_str(8)
		temp = open('docs/' + str + '.html', 'w')
		temp.write(prefix)
		temp.write(name + "<br>" + subject + "<br>" + date + "<br>" + perstr + "<br><br>")
		temp.write('</div><div id="title"; align="center">' + title + '<br><br></div><div id="content"; align="left">')
		for line in f:
			temp.write(line)
		temp.write('</div>')
		f.close()
		os.system("rm -f " + str + ".txt")
		temp.close()
		val = {
				"URL": "http://hunterlang.com/doc/docs/" + str + ".html",

			}
		self.finish(val)
	
def rand_str(leng):
    nbits = leng * 6 + 1
    bits = random.getrandbits(nbits)
    uc = u"%0x" % bits
    newlen = int(len(uc) / 2) * 2 # we have to make the string an even length
    ba = bytearray.fromhex(uc[:newlen])
    return base64.urlsafe_b64encode(str(ba))[:leng]
def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
    main()
