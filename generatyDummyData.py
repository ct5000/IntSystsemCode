import psycopg2


def getSqlString(name, time, position = None, windSpeed = None, windDirection = None, heading = None, speed = None):
    sqlFirstLine = """INSERT INTO boatdata(name, time"""
    sqlSecondLine = """ VALUES('%s','%s'""" % (name, time)
    if position != None:
        sqlFirstLine += """,position"""
        sqlSecondLine += """,'%s'""" % position
    if windSpeed != None:
        sqlFirstLine += """,windSpeed"""
        sqlSecondLine += """,'%f'""" % windSpeed
    if windDirection != None:
        sqlFirstLine += """,windDirection"""
        sqlSecondLine += """,'%d'""" % windDirection
    if heading != None:
        sqlFirstLine += """,heading"""
        sqlSecondLine += """,'%d'""" % heading
    if speed != None:
        sqlFirstLine += """,speed"""
        sqlSecondLine += """,'%f'""" % speed
    sql = sqlFirstLine + """)""" + sqlSecondLine + """);"""
    return sql

conn = psycopg2.connect(database = "intproject", 
                        host = "localhost",
                        user = "intproject",
                        password = "project1234")


cursor = conn.cursor()
# For test of single entry
sql = getSqlString(name="Stormfuglen",time='2022-01-01 01:24:53+02',position='10.001,55.999',windSpeed=7.6,windDirection=270,heading=180,speed=4.5)
#print(sql)
cursor.execute(sql)

sql = getSqlString(name="Ternen",time='2022-01-01 01:24:53+02',position='10.001,55.999',windSpeed=5.6,windDirection=270,heading=180,speed=4.5)
#print(sql)
cursor.execute(sql)

cursor.execute("SELECT * FROM boatdata")
print(cursor.fetchall())
conn.commit()

'''
# For full generation of data

datapoints = 10000

# Create data for first boat
boatName1 = "Stormfuglen"
for i in range(datapoints):
  




# Create data for second boat
boatName2 = "Jack"


'''



conn.close()




