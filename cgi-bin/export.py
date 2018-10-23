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
<p>The input date is: %s</p>
<p>The input city is: %s</p>
<hr>"""

date = form['date'].value
city = form['citys'].value
print(html % ("hello, what's up?", date, city))
