from datetime import datetime as dt
from datetime import timedelta
import time
import pyodbc
import os
import inspect

conn=r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\CAL_DB.accdb;' #PATHNAME
conn = pyodbc.connect(conn)  #DB Connector
cursor = conn.cursor() #Table Adapter / DB Cursor

def study_materials():



    # year,month,day - hour,minute,second,
    # source: https://www.saltycrane.com/blog/2008/11/python-datetime-time-conversions/
    # tuple to string format
    time_tuple = (2018, 1, 13, 0, 51, 18, 0,315, 1)
    time2_tuple = (2018, 1, 13, 13, 50, 18, 2, 317, 0)

    print("tuple to String")
    date_str = time.strftime("%Y-%m-%a %H:%M:%S", time_tuple)
    print(date_str)
    print()

    # string to tuple format
    print("String to tuple")
    date_str = "2008-11-10 17:53:59"
    time_tuple = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    print(time_tuple)
    print(time_tuple[0:9])
    print()
    # ------------------------------------
    # source: https://stackoverflow.com/questions/3096953/how-to-calculate-the-time-interval-between-two-time-strings
    # time subtraction
    print("Time Subtraction")
    time_tuple = (2018, 1, 13, 13, 51, 18, 2, 317, 0)
    time2_tuple = (2018, 1, 10, 13, 50, 19, 2, 317, 0)
    s1 = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
    s2 = time.strftime("%Y-%m-%d %H:%M:%S", time2_tuple)
    FMT = '%Y-%m-%d %H:%M:%S'
    tdelta = dt.strptime(s2, FMT) - dt.strptime(s1, FMT)
    print(tdelta)

    def days_hours_minutes_second(delta):
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds % 60
        return 0,0,days,hours,minutes,seconds,2, 317, 0

    print(days_hours_minutes_second(tdelta))

    print("--------------------------------")

    def time_array_to_string_print(time_array):
        date_str = time.strftime("%A %d %H:%M:%S", time_array)
        return date_str

    time_tuple = (2018, 1, 2, 13, 51, 18, 2, 317, 0)
    date_str = time_array_to_string_print(time_tuple)
    print(date_str)

def time_array_to_hour(time_array):
    def get_hour(time_str):
        h, m, s = time_str.split(':')
        return int(h) + int(m) / 60.0 + int(s) / 3600.0  # returns as double

    date_str = time.strftime("%H:%M:%S", time_array)
    hour = get_hour(date_str)
    print(hour)

time_array_to_hour((2018, 1, 1, 21, 30, 0, 0, 317, 0))



