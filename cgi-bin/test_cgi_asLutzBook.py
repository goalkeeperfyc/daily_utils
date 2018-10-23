#!/usr/bin/python
# -*- coding: utf-8 -*-

import cgi
form = cgi.FieldStorage()

print("Content-type: text/html\n")

html = """
<title>CGI script</title>
<h1>Greetings</h1>
<hr>
<p>%s</p>
<hr>"""

print(html % "hello, what's up?")
