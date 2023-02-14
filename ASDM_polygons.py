import cgitb
import cgi
import folium
import cx_Oracle

#with open("../../oracle",'r') as pwf:
    #pw = pwf.readline().strip()
    

map_l = folium.Map(location=[55.9486,-3.2008],zoom_start=12)

conn = cx_Oracle.connect(dsn="geoslearn",user="s2318635",password="rutuja")

c = conn.cursor()
query = ("select OGR_FID, TO_CHAR(D.ORA_GEOMETRY.GET_WKT()) from DATAZONE D")
#c.execute("select FID, st_aswkt(GEOMETRY) from datazone")
c.execute(query)
polygons = c.fetchall()

for polygon in polygons :
    OGR_FID, charwkt = polygon
    folium.Polygon(charwkt, color = "red", fill_color="red", fill_opacity=0.5).add_to(map_l)

print("Content-type: text/html\n")
#
print(map_l.get_root().render()) 

map_l.save("datazone.html")
