import cgitb
import cgi
import folium
import cx_Oracle



coords = []
lon = []
lat= []


map_l = folium.Map(location=[55.9486,-3.2008],zoom_start=12)

conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password="rutuja")

c = conn.cursor()
query = ("""SELECT OGR_FID, SDO_UTIL.TO_WKTGEOMETRY(SDO_CS.TRANSFORM("ORA_GEOMETRY", 4326))FROM GREENSPACE WHERE 'distName1' = 'Inverleith Park'""")
output = c.execute(query)
for row in output:
    polygon_fid = row[0]
    polygon = row[1].read().split()
    for i in range(1, len(polygon)-1, 2):
        lon.append(float(polygon[i].strip()))
        lat.append(float(polygon[i+1].strip()))

    for i in range(0, len(lon)-1):
        coords.append(lat[i], lon[i])

    folium.Polygon(locations = coords, popup = str(polygon_fid), color = "red", fill_color="red", fill_opacity=0.5).add_to(map_l)

# print("Content-type: text/html\n")

# print(map_l.get_root().render()) 

# map_l.save("datazone.html")