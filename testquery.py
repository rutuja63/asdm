#!/usr/bin/env python3

"""A webpage that generates a form and submits values to query on the server"""
import cx_Oracle
import re
import folium
import cgi
import cgitb
cgitb.enable()

print("Content-Type: text/html\n")
print("<!DOCTYPE html>")
print("<head>")
print("<title>Test form for SQL query</title>")
print("</head>")

print("<body>")

#connect to the server and retrieve the values from the table

#uncomment the below and add your username and password
#conn = cx_Oracle.connect("uname/passwd@geoslearn")
c = conn.cursor()
c.execute("SELECT G.\"distName1\" FROM S2318635.GREENSPACE G")
print("<h3>Find cafes near a selected greenspace</h3>")
print("<form name=\"query1\" action=\"\" method=\"get\">")
print("Select Greenspace: <input list=\"gspaces\"  name=\"gspace\">")
print("<datalist id=\"gspaces\">")
for x in c:
    x = re.sub(r'[(),\'\"]', '', str(x))
    optn = "<option value=\"{}\">"
    print(optn.format(x))
print("</datalist>")
print("<input type=\"submit\" value=\"Submit\">")
print("</form>")
conn.close()

#The section below does not work

form = cgi.FieldStorage()
qterm = form.getvalue('gspace')

#uncomment below and add your username and password
#conn = cx_Oracle.connect("uname/passwd@geoslearn")
d = conn.cursor()
d.execute("SELECT /**ORDERED*/C.NAME, C.TELEPHONE, .POSTCODE FROM S2318635.CAFES C, S2318635.GREENSPACE G WHERE G.\"distName1\" = "+str(qterm)+" AND SDO_WITHIN_DISTANCE(C.ORA_GEOMETRY, G.ORA_GEOMETRY,'distance=0.3/0.6/1.0/ UNIT = mile')=TRUE")

for r in d:
    print(r)

conn.close()

print("</body>")
print("</html>")
