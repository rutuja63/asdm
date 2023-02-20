#!/usr/bin/env python3
import cgi,sys
import cgitb
import folium
import cx_Oracle

cgitb.enable()
form = cgi.FieldStorage()

with open("../../oracle","r") as pwf:
    pw = pwf.read().strip()
map = folium.Map(location=[55.9486,-3.2008],zoom_start=14)
folium.LayerControl().add_to(map)

Name = form.getvalue('POLYGON NAME2')
conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password=pw)

query = ("""SELECT SDO_UTIL.TO_WKTGEOMETRY(WALKPOINTS1.ORA_GEOM), SDO_UTIL.TO_WKTGEOMETRY(DATAZONE.ORA_GEOM)
            FROM DATAZONE, WALKPOINTS1
            WHERE 
            DATAZONE.NAME = '%s'
            AND
            SDO_GEOM.SDO_INSIDE(WALKPOINTS1.ORA_GEOM,DATAZONE.ORA_GEOM)='TRUE'
            """)%(Name)
c = conn.cursor()

c.execute(query)

result = c.fetchall()

i = 0
point = []
polygon = []
DS = []
for element in result:
    DS.append(result[i][0])
    pt = result[i][1].read()
    pl = result[i][2].read()
    pt= pt.strip('POLYGON INT')
    pt = pt.strip('() ').split(',')
    pl= pl.strip('POLYGON INT')
    pl = pl.strip('() ').split(',')
    point.append(pt)
    polygon.append(pl)
    i = i + 1

DS = ("%.2f" %DS[0])
txt = ('Distance is ' + str(DS) +' m')

for element in point: 
    node = element[0].strip(' ').split(' ')
    x = float(node[1])
    y = float(node[0])

    folium.Marker(location=[x,y],popup=txt,icon=folium.Icon(color='darkred')).add_to(map)

for element in polygon: 
    composite_list=[]
    poly = []
    n = 0
    while n < len(element):
        node = element[n].strip(' ').split(' ')
        poly.append(float(node[1]))
        poly.append(float(node[0]))
        n = n + 1
    test = poly
    composite_list = [test[x:x+2] for x in range(0, len(test),2)]
    folium.Polygon(composite_list,popup=txt, color='darkred', fill= True, fill_color='blue').add_to(map)

print("Content-type: text/html\n")
print(map.get_root().render())
