#!/usr/bin/env python
# Pass this application the path to an uploaded document. It prints the path of the newly created HTML file.
# Copyright Hunter Lang 2011
# ************** Assumes all paths start with 'doc/' *****************
# MIT Liscense
import sys
import os
import os.path
import commands
import random
import base64
from pyPdf import PdfFileWriter, PdfFileReader
def main(argv):
	path = argv[1]
	name = argv[2]
	subject = argv[3]
	period = argv[4]
	title = argv[5]
	path_to_text = identify(path)
	to_html(path_to_text, name, subject, period, title)
	
def identify(path):
	ext = os.path.splitext(path)[1]
	filename = os.path.splitext(path)[0]
	if ext == ".doc" or ext == ".docx":
		return word(path, filename)
	elif ext == ".pages":
		return pages(path, filename)
	elif ext == ".odt":
		return odt(path, filename)
	elif ext == ".pdf":
		return pdf(path, filename)
	else:
		print "Fatal Error: conversion failed - file type " + ext + " is not supported."
		exit()

def pages(path, filename):
	os.rename("docs/" + path, "docs/" + filename + ".zip")
	commands.getstatusoutput('unzip -j docs/' + filename + ".zip" + ' QuickLook/Preview.pdf')
	rand = rand_pretty_str(10)
	commands.getstatusoutput('mv Preview.pdf docs/' + rand + '.pdf')
	pdf = PdfFileReader(open("docs/" + rand + ".pdf", "rb"))
	n = open("docs/" + filename + ".txt", "wb")
	for page in pdf.pages:
		n.write(page.extractText())
	n.close()
	return "docs/" + filename + ".txt"

def word(path, filename):
	commands.getstatusoutput('textutil -convert txt docs/' + path)
	return "docs/" + filename + ".txt"

def odt(path, filename):
	print "odt"

def pdf(path, filename):
	input_file = PdfFileReader(file("docs/" + path, "rb"))
	f = open("docs/" + filename + ".txt", 'wb')
	for page in input_file.pages:
		f.write(page.extractText())
	return "docs/" + filename + ".txt"



def to_html(path, name, subject, period, title):
	input_file = open(path, 'rb')
	rand = rand_str(8)
	output = open("docs/" + rand + ".html", 'wb')
	pref = open('prefix.txt')
	prefix = pref.read()
	date = "March 5"
	perstr = "Period " + period
	output.write(prefix)
	output.write(name + "<br>" + subject + "<br>" + date + "<br>" + perstr + "<br><br>")
	output.write('</div><div id="title"; align="center">' + title + '<br><br></div><div id="content"; align="left">')
	for line in input_file:
		output.write(line)
	output.write('</div>')
	input_file.close()
	output.close()
	print "docs/" + rand + ".html"
	
	

def rand_pretty_str(leng):
	chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefhijklmnopqrstuvwxtttyz0123456789"
	str = ""
	for i in range(leng):
		str += chars[random.randint(0, 62)]
	return str	
def rand_str(leng):
    nbits = leng * 6 + 1
    bits = random.getrandbits(nbits)
    uc = u"%0x" % bits
    newlen = int(len(uc) / 2) * 2 # we have to make the string an even length
    ba = bytearray.fromhex(uc[:newlen])
    return base64.urlsafe_b64encode(str(ba))[:leng]
	
if __name__ == "__main__":
    main(sys.argv)