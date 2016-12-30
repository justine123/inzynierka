# Create your tasks here
import socket
import sys
import json
import datetime
from .models import Sensor, Entry
from background_task import background


@background(schedule=60)
def get_data_from_rpi():
    """
    Get entries data from Raspberry PI and save them into database
    """
    print("Server started!")
    sensor_data = []
    host = ''
    port = 8888
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((host, port))  # Bind socket to local host and port
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    s.listen(10)  # Start listening on socket
    while 1:
        conn, addr = s.accept()  # wait to accept a connection - blocking call
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        line = conn.recv(1024)
        message = ''
        while line:
            print "Receiving Data..."
            message += line
            line = conn.recv(1024)
            print "message:", message
            if message.endswith("}"):
                sensor_data.append(json.loads(message))
                print "sensor data:", sensor_data
                message = ''
            print "Done Receiving"
        for data in sensor_data:
            sensor = Sensor.objects.get(sensor_id=data['sensor_id'])
            for key, value in data.items():
                if value == '':
                    data[key] = None  # for the IntegerField in Entry model...
            # print data
            entry = Entry.objects.create(sensor=sensor,
                          date=datetime.datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S"),
                          temperature=data['temperature'],
                          humidity=data['humidity'],
                          pm25=data['pm2.5'],
                          pm10=data['pm10'],
                          pressure=data['pressure'],
                          wind_speed=data['wind_speed'],
                          wind_direction=data['wind_direction'])
            print "Received data from" + entry.date
            # entry.save()
        print len(Entry.objects.all())
    s.close()
