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
print("<title>Restaurants near greenspaces</title>")
print("</head>")

print("<body>")

#connect to the server and retrieve the values from the table

#uncomment the below and add your username and password
#conn = cx_Oracle.connect("username/password@geoslearn")
c = conn.cursor()
c.execute("SELECT /**ORDERED*/G.NAME FROM S2318635.GREENSPACE G")
print("<h3>Find restaurants near a selected greenspace</h3>")
print("<form name=\"query1\" action=\"testquery.py\" method=\"get\">")
print("Select Greenspace: <input list=\"gspaces\"  name=\"gspace\" placeholder=\"click to select\">")
print("<datalist id=\"gspaces\">")
for x in c:
    #x = re.sub(r'[(),\'\"]', '', str(x))
    optn = "<option value=\"{}\">"
    print(optn.format(x[0]))
print("</datalist>")
print("<input type=\"submit\" value=\"Submit\">")
print("</form>")
conn.close()



form = cgi.FieldStorage()
qterm = form.getvalue('gspace')


#use a 'try'/'except' loop to handle errors generated before a value is selected
try:
    print('<h4>Restaurants near '+qterm+': </h4>')


    #uncomment below and add your username and password
    #conn = cx_Oracle.connect("username/password@geoslearn")

    #connect to oracle and run the query
    d = conn.cursor()
    d.execute("SELECT /**ORDERED*/C.NAME, C.TELEPHONE, C.POSTCODE FROM S2318635.CAFES C, S2318635.GREENSPACE G WHERE G.NAME = \'"+qterm+"\' AND SDO_WITHIN_DISTANCE(C.ORA_GEOMETRY, G.ORA_GEOMETRY,'distance=0.3/0.6/1.0/ UNIT = mile')=\'TRUE\'")
    

    #print the results on the page
    for row in d:
        
        print(row[0] + ' - ' + row[1] + ' - ' + row[2]+'<br>')

    conn.close()

except:
    print('')

print("</body>")
print("</html>")
