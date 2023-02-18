#!/usr/bin/env python3
import cgi,os,sys
import cgitb
import folium
import cx_Oracle

# os.environ['QUERY_STRING']="PARK_NAME=''&Distance= "

# def query1():
#     return "SELECT R.NAME, SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(R.ORA_GEOMETRY, 4326)) FROM S2434646.RESTAURANTS R, GREENSPACE G WHERE G.NAME = '%s' AND SDO_NN(R.ORA_GEOMETRY, SDO_GEOM_MBR(G.ORA_GEOMETRY), 'sdo_num_res = %s') = 'TRUE'"%(name,number)

def query3():
    return "SELECT WALKPOINTS1.NAME, SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(WALKPOINTS1.ORA_GEOMETRY, 4326))FROM WALKPOINTS1, STREET WHERE STREET.NAME = '%s' AND SDO_RELATE(WALKPOINTS1.ORA_GEOMETRY, SDO_GEOM.SDO_BUFFER(STREET.ORA_GEOMETRY, %s, 0.005), 'MASK=ANYINTERACT') = 'TRUE' "%(name,distance)
cgitb.enable()
try:
    form =  cgi.FieldStorage()
    name = form.getvalue("Streetname")
    # number = form.getvalue("nearest")
    distance = form.getvalue("distance")


    map_l = folium.Map(location=[55.9480,-3.2008],zoom_start=15)
    conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password="rutuja")
    c = conn.cursor()


    c.execute(query3())


    coordPoints = []
    for row in c:
        point_name = row[0]
        point = row[1].read()
        coordinates = point.lstrip("POINT (").rstrip(")")
        coordPoints.append([point_name,[float(coord) for coord in coordinates.split(" ")]])
    for element in coordPoints:
       folium.Marker(location = [element[1][1],element[1][0]], popup = str(element[0])).add_to(map_l)
    c.close()

    print("Content-Type: text/html\n")
    print(query3())
    print(map_l.get_root().render()) 
    # map_l.save("test.html")
except:
    print("Content-Type: text/html\n")
    print(cgitb.html(sys.exc_info()))

