#!/usr/bin/env python3
import cgi, sys
import cgitb
import folium
import cx_Oracle
def query5():
    return "SELECT G.NAME, G.\"Shape_Area\", SDO_UTIL.TO_WKTGEOMETRY(G.ORA_GEOMETRY) FROM GREENSPACE G,DATAZONE D  WHERE D.\"Name\"  = '%s' AND SDO_OVERLAPS(G.ORA_GEOMETRY, D.ORA_GEOMETRY)='TRUE'" %(datazone)

cgitb.enable()
try:
    form =  cgi.FieldStorage()
    datazone = form.getvalue("datazone")
   
    map_l = folium.Map(location=[55.9486,-3.2008],zoom_start=12)
    conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password="rutuja")
    c = conn.cursor()
    c.execute(query5())

    coordsInpolygons = []
    for row in c:
        coordsInpolygon = []
        polygon_fid = row[0]
        polygon = row[2].read()

        coordinates = polygon.lstrip("POLYGON ((").rstrip("))").split(", ")
        for element in coordinates:
            coordinate = element.split(" ")
            lon = coordinate[0]
            lat = coordinate[1]
        
            coordInPolygon = [float(lat), float(lon)]
            coordsInpolygon.append(coordInPolygon)
        coordsInpolygons.append([polygon_fid, coordsInpolygon])

    for element in coordsInpolygons:
        folium.Polygon(locations = element[1], popup = str(element[0]), color = "red", fill_color="red", fill_opacity=0.5).add_to(map_l)
    c.close()

    print("Content-Type: text/html\n")
    print(map_l.get_root().render()) 
    map_l.save("test.html")

except:
    print("Content-Type: text/html\n")
    print(cgitb.html(sys.exc_info()))
