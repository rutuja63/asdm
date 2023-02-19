#!/usr/bin/env python3
import cgi,os,sys
import cgitb
import folium
import cx_Oracle

def query4():
    return "SELECT g.NAME, sdo_nn_distance (1) distance_in_miles, SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(g.ORA_GEOMETRY, 4326)) FROM STREET s , GREENSPACE g WHERE s.NAME = '%s' AND sdo_nn(g.ORA_GEOMETRY, s.ORA_GEOMETRY ,'sdo_num_res=2 unit= mile', 1) = 'TRUE' ORDER BY distance_in_miles"%(name)

cgitb.enable()

try:
    form = cgi.FieldStorage()
    name = form.getvalue("Streetname")
    


    map_l = folium.Map(location=[55.9480,-3.2008],zoom_start=15)
    conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password="rutuja")
    c = conn.cursor()
    c.execute(query4())


    coordsInpolygons = []
    for row in c:
        coordsInpolygon = []
        gname = row[0]
        distance = row[1]
        polygon = row[2].read()
       
        coordinates = polygon.lstrip("POLYGON ((").rstrip("))").split(", ")
        for element in coordinates:
            coordinate = element.split(" ")
            lon = coordinate[0]
            lat = coordinate[1]
        
        coordInPolygon = [float(lat), float(lon)]
        coordsInpolygon.append(coordInPolygon)
    coordsInpolygons.append([gname, distance, coordsInpolygon])

    for element in coordsInpolygons:
        folium.Polygon(locations = element[2], popup = str(element[0]), color = "red", fill_color="red", fill_opacity=0.5).add_to(map_l)

    c.close()
    
    print("Content-Type: text/html\n")
    print(query4())
    print(map_l.get_root().render()) 
    # map_l.save("test.html")
except:
    print("Content-Type: text/html\n")
    print(cgitb.html(sys.exc_info()))
    print(query4())


