"""query to find bus stops in datazones that interact with a grespace"""

import cx_Oracle
import sys
import re
import folium
import cgi
import cgitb


#import greenspace id from form

#first query to find datazones that have spatial interaction with the selected greenspace
def query6a():
    return "SELECT D.OGR_FID FROM S2318635.DATAZONE D, S2318635.GREENSPACE G WHERE G.OGR_FID = %s AND SDO_ANYINTERACT(D.ORA_GEOMETRY , G.ORA_GEOMETRY)='TRUE'"%(parkId)

#second query to find the restaurants inside the datazones from the first query
def query6b():
    return "SELECT C.NAME, C.URL, C.TELEPHONE, SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(C.ORA_GEOMETRY, 4326)) FROM S2318635.DATAZONE D, S2318635.CAFES C WHERE D.OGR_FID = %s AND SDO_INSIDE(C.ORA_GEOMETRY, D.ORA_GEOMETRY)='TRUE'"%(dz_id)

cgitb.enable()

try:
    form = cgi.FieldStorage()
    parkId = form.getvalue("PARK_ID") 
    
    #uncomment to test code without a form input
    #parkId = 1

    #generate empty map of Edinburgh
    map_1 = folium.Map(location=[55.9480,-3.2008],zoom_start=13)

    #connect to the server
    conn = cx_Oracle.connect("username/password@geoslearn") #put a correct username and password

    c = conn.cursor()
    
    #run the first query
    c.execute(query6a())
    
    #loop over query resutls and execute the second query to find restaurants in the relatd datazones
    for x in c:
        dz_id = x
        d = conn.cursor()

        d.execute(query6b())
        #create empty array for the information pulled from query 2
        coordPoints = []
        
        #loop over the results and append them to the array
        for row in d:
            point_name = row[0]
            point_type = row[1]
            point_tele = row[2]
            points = row[3].read()
            coordinates = points.lstrip("POINT (").rstrip(")")
            coordPoints.append([point_name, point_type, point_tele, [float(coord) for coord in coordinates.split(" ")]])

        #populate the map and popups with information from the query
        for element in coordPoints:
            folium.Marker(location = [element[3][1],element[3][0]], popup = '<a href="https://'+str(element[1])+'" target="blank">'+str(element[0])+'</a><br><br>Tel: '+element[2]).add_to(map_1)
        conn.close
    
    print("<Content-Type: text/html><br>")
    print(map_1.get_root().render())
    




    

except:
    print("<Content-Type: text/html><br>")
    print(cgitb.html(sys.exc_info()))
