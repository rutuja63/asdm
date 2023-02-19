"""query to find bus stops in datazones that interact with a grespace"""

import cx_Oracle
import sys
import re
import folium
import cgi
import cgitb


"import greenspace id from form"
def query6a():
    return "SELECT D.OGR_FID FROM S2318635.DATAZONE D, S2318635.GREENSPACE G WHERE G.OGR_FID = %s AND SDO_ANYINTERACT(D.ORA_GEOMETRY , G.ORA_GEOMETRY)='TRUE'"%(parkId)

def query6b():
    return "SELECT C.NAME, C.\"TYPE\", SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(C.ORA_GEOMETRY, 4326)) FROM S2318635.DATAZONE D, S2318635.CAFES C WHERE D.OGR_FID = %s AND SDO_INSIDE(C.ORA_GEOMETRY, D.ORA_GEOMETRY)='TRUE'"%(dz_id)

cgitb.enable()

try:
    form = cgi.FieldStorage()
    parkId = form.getvalue("PARK_ID") 
    #parkId = 7  

    
    map_1 = folium.Map(location=[55.9480,-3.2008],zoom_start=15)

    conn = cx_Oracle.connect("########/#password#@geoslearn") #put a correct username and password

    c = conn.cursor()
    
    c.execute(query6a())
    #c.close()

    for x in c:
        dz_id = x
        d = conn.cursor()

        d.execute(query6b())
        coordPoints = []
        for row in d:
            point_name = row[0]
            point_type = row[1]
            points = row[2].read()
            coordinates = points.lstrip("POINT (").rstrip(")")
            coordPoints.append([point_name, point_type,[float(coord) for coord in coordinates.split(" ")]])

        for element in coordPoints:
            folium.Marker(location = [element[2][1],element[2][0]], popup = str(element[0])+' '+str(element[1])).add_to(map_1)
        d.close
    
    print("Content-Type: text/html\n")
    print(map_1.get_root().render())




    

except:
    print("Content-Type: text/html\n")
    print(cgitb.html(sys.exc_info()))
