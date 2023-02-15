import cgitb
import cgi
import folium
import cx_Oracle




map_l = folium.Map(location=[55.9486,-3.2008],zoom_start=12)

conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password="rutuja")

c = conn.cursor()
query = "SELECT OGR_FID , SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(ORA_GEOMETRY, 4326)) FROM CAFES"
c.execute(query)



coordPoints = []
for row in c:
    point_name = row[0]
    point = row[1].read()

    coordinates = point.lstrip("POINT (").rstrip(")")
    coordPoints.append([float(coord) for coord in coordinates.split(" ")])

# print(coordPoints)


for element in coordPoints:
    folium.Marker(location = [element[1],element[0]], popup = str(point_name)).add_to(map_l)



print("Content-type: text/html\n")

print(map_l.get_root().render()) 

map_l.save("cafes.html")