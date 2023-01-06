import psycopg2
import math
import random

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

def convertCompas2rad(compas):
    degree = ((-1)*compas + 90)%360
    return degree * math.pi / 180




def convertSecondToString(time):
    seconds = time % 60
    hours = math.floor(time/3600)
    minutes = math.floor(((time/3600) - hours) * 60)
    txt = "{:02d}:{:02d}:{:02d}".format(hours,minutes,seconds)
    return txt

conn = psycopg2.connect(database = "intproject", 
                        host = "localhost",
                        user = "intproject",
                        password = "project1234")

cursor = conn.cursor()
'''
# For test of single entry
sql = getSqlString(name="Stormfuglen",time='2022-01-01 01:24:53+02',position='10.001,55.999',windSpeed=7.6,windDirection=270,heading=180,speed=4.5)
#print(sql)
cursor.execute(sql)

#sql = getSqlString(name="Ternen",time='2022-01-01 01:24:53+02',position='10.001,55.999',windSpeed=5.6,windDirection=270,heading=180)
#print(sql)
#cursor.execute(sql)

cursor.execute("SELECT * FROM boatdata")
data = cursor.fetchall()
print(data)
print(type(data[0][4]))
#conn.commit()


'''
# For full generation of data


datapoints = 1000

# Create data for first boat
boatName1 = "Stormfuglen"
date = '2022-01-05 '
time = 6000
time_step = 15
wind_speed = 5
wind_direction = 300
speed = 2.5
lat = 56.
long = 10.5
heading = 210
for i in range(datapoints):
    hour_str = convertSecondToString(time)
    time_str = date + hour_str + "+01"
    position_str = "%f,%f" % (lat,long)
    speed_noise = speed + random.normalvariate(mu=0,sigma=0.1)
    wind_speed_noise = wind_speed + random.normalvariate(mu=0,sigma=0.1)
    heading_noise = heading + random.randint(-2,2)
    wind_direction_noise = wind_direction + random.randint(-2,2)
    sql = getSqlString(name=boatName1,time=time_str,position=position_str,windSpeed=wind_speed_noise,windDirection=wind_direction_noise,heading=heading_noise,speed=speed_noise)
    cursor.execute(sql)
    time = time + time_step
    long = long + speed * time_step * (1/55800) * math.cos(convertCompas2rad(heading))
    lat = lat + speed * time_step * (1/111412) * math.sin(convertCompas2rad(heading))





# Create data for second boat
'''
boatName2 = "Jack"

for i in range(datapoints):
    hour_str = convertSecondToString(time)
    time_str = date + hour_str + "+01"
    position_str = "%f,%f" % (lat,long)
    sql = getSqlString(name=boatName2,time=time_str,position=position_str,windSpeed=wind_speed,windDirection=wind_direction,heading=heading,speed=speed)
    cursor.execute(sql)
    time = time + time_step
    long = long + speed * time_step * (1/55800)
'''
cursor.execute("SELECT * FROM boatdata")
data = cursor.fetchall()
print(data[0:10])
conn.commit()




conn.close()




