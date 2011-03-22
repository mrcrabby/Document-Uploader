#!/usr/bin/env python
#
# Copyright 2011 Hunter Lang
#
# MIT Liscence
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


from tornado.options import define, options

define("port", default=8019, help="run on the given port", type=int)

# This defines the applications routes
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
			(r"/", IndexHandler),
			(r"/static", IndexHandler),
			(r"/test", TestHandler),

			
        ]
        
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.redirect("/static/index.html")

class TestHandler(tornado.web.RequestHandler):
	@tornado.web.asynchronous
	def post(self):
		file_content = self.request.files['file'][0]
		file_body = file_content['body']
		filename = file_content['filename']		
		random_file_name = rand_str(8) + os.path.splitext(filename)[1]
		output_file = open("docs/" + random_file_name, 'w')
		output_file.write(file_body)
		output_file.close()
		path = random_file_name
		name = 'Hunter Lang'
		subject = 'English 9 Honors'
		var = commands.getstatusoutput('python core.py ' + path + ' Hunter\ Lang' + ' English\ 9\ Honors' + ' 4' + ' test')
		print var[1]
		if var[1][-5:] != ".html":
			val = {
				"URL": "Something went wrong during conversion. Make sure you're adhering to the guidelines in the Upload Guide, and if problems persist, contact me."
			}
			self.finish(val)
		else:
			val = {
				"URL": "http://hunterlang.com/doc/" + var[1]
			}
			self.finish(val)
	def terminalize(string):
		string.replace(' ', '\ ')
		return string

	
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
