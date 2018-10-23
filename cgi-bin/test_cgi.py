#!/usr/bin/python3
# -*- coding: utf-8 -*-
#import cgi
#import cgitb

#cgitb.enable(display=0, logdir="/var/log/cig/cig_test_log")
#cgitb.enable()

print("Content-Type: text/html\r\n")
print()

print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
print("Hello CGI!")

#form = cgi.FieldStorage()
#if "name" not in form or "addr" not in form:
#    print("<H1>Error!</H1>")
#    print("Please fill in the name and addr fields.")
#    return
#print("<p>name:", form["name"].value)
#print("<p>addr:", form["addr"].value)
