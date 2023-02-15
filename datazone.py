import cgitb
import cgi
import folium
import cx_Oracle




map_l = folium.Map(location=[55.9486,-3.2008],zoom_start=12)

conn = cx_Oracle.connect(dsn="geoslearn",user="#######",password="#######")

c = conn.cursor()
query = "SELECT OGR_FID , SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM(ORA_GEOMETRY, 4326)) FROM DATAZONE"
c.execute(query)

# for row in c:
#     print(row[0])
#     print(row[1].read())

coordsInpolygons = []
for row in c:
    coordsInpolygon = []
    polygon_fid = row[0]
    polygon = row[1].read()

    coordinates = polygon.lstrip("POLYGON ((").rstrip("))").split(", ")
    for element in coordinates:
        coordinate = element.split(" ")
        lon = coordinate[0]
        lat = coordinate[1]
        
        coordInPolygon = [float(lat), float(lon)]
        coordsInpolygon.append(coordInPolygon)
    coordsInpolygons.append(coordsInpolygon)
print(coordsInpolygons)

for element in coordsInpolygons:
    folium.Polygon(locations = element, popup = str(polygon_fid), color = "red", fill_color="red", fill_opacity=0.5).add_to(map_l)


    # for i in range(1, len(polygon)-1, 2):
    #     lon.append(float(polygon[i].strip('((').split()))
    #     lat.append(float(polygon[i+1].strip('))')))
    # print(lon)
    # for i in range(0, len(lon)-1):
    #     coords.append(lat[i], lon[i])
    # print(lon)

# folium.Polygon(locations = coordsInpolygon, popup = str(polygon_fid), color = "red", fill_color="red", fill_opacity=0.5).add_to(map_l)

print("Content-type: text/html\n")

print(map_l.get_root().render()) 

map_l.save("DATAZONE.html")