#!/usr/bin/python3
print("Content-Type: text/html")
print()

print("<TITLE>CGI script output</TITLE>")
print("<H1>This is my first CGI script</H1>")
print("Hello CGI!")

input_form = """<form>
query string: 
<input type="text" name="query_str">
<br />
date: 
<input type="text" name="date">
<br />
CSM citys: 
<input type="text" name="csm_citys">
<br />
OTT ciyts: 
<input type="text" name="ott_ciyts">
<br />





<br />
<input type="submit" value="Confirm Submit">
</form>"""
print(input_form)

