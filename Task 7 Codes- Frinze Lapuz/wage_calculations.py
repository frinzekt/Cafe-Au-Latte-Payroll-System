#Wage_calculations
#   This file is responsible in Clock-in, Clock-out, Calculating wages
#
# Name: Frinze Lapuz

import pyodbc #db
import inspect
import os     #os manipulation, directories path
import random #random number generator
import sys    #cmd access (windows cmd in the future)
import locale #currency
import re     #alphanumeric limitation
from datetime import datetime as dt
import time

import Internal_Processing
import import_export

#set currency Dollars
locale.setlocale(locale.LC_ALL,'')


conn=r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\CAL_DB.accdb;' #PATHNAME
conn = pyodbc.connect(conn)  #DB Connector
cursor = conn.cursor() #Table Adapter / DB Cursor
def display(Employee_ID):
    choices = {}
    choices[0] = "Clock-In"
    choices[1] = "Clock-Out"
    choices[2] = "Calculate your wage"
    choices[3] = "Go back to previous menu"

    Internal_Processing.header("CLOCK-IN | CLOCK-OUT | CALCULATE WAGE")
    choice = Internal_Processing.select(choices,"Please select from the functionalities below:")

    if choice == 0:
        Internal_Processing.header("CLOCK-IN")
        clock_in(Employee_ID)
    elif choice == 1:
        Internal_Processing.header("CLOCK-OUT")
        clock_out(Employee_ID)
    elif choice == 2:
        Internal_Processing.header("CALCULATE YOUR WAGE")
        Calculate_Wage_One_Person(Employee_ID)
    elif choice == 3:
        Internal_Processing.display_menu()

def Calculate_Wage_One_Person(Employee_ID):
    #CALCULATES WAGE FOR THE EMPLOYEE THAT CALLED THIS FUNCTION
    weekdays_short = {}
    weekdays_short[0] = "Mon"
    weekdays_short[1] = "Tue"
    weekdays_short[2] = "Wed"
    weekdays_short[3] = "Thu"
    weekdays_short[4] = "Fri"
    weekdays_short[5] = "Sat"
    weekdays_short[6] = "Sun"

    sql_select = "SELECT RoleID,Sup_an,Helt_Ins FROM Employee WHERE ID=" + str(Employee_ID)
    cursor.execute(sql_select)
    row= cursor.fetchall()  # one row only

    Employee_RoleID = row[0][0]
    Employee_Sup_an = row[0][1]
    Employee_Helt_Ins= row[0][2]


    #SQL COMPLETION
    sql_calcultion = "SELECT MonH,TueH,WedH,ThuH,FriH,SatH,SunH,MonOH,TueOH,WedOH,ThuOH,FriOH,SatOH,SunOH FROM Calculation WHERE EmployeeID=" + str(
        Employee_ID)  # EmployeeID
    cursor.execute(sql_calcultion)
    row_calculation = cursor.fetchall()  # one row only

    row_norm_hours = {}
    row_ot_hours = {}

    #print(sql_calcultion)
    #print(row_calculation)
    for col in range(7): #EXTRACTS VALUES FROM TABLE
        row_norm_hours[col] = row_calculation[0][col]
        row_ot_hours[col] = row_calculation[0][col + 7]

    # print("Row_norm_ho",row_norm_hours)
    # print("Row_ot_ho",row_ot_hours)

    #EXTRACTS MULTIPLE VALUES FROM THE RETURN OF GROSSPAY
    gross_total_norm_hour_total_ot_hour = GrossPay(Employee_RoleID, row_norm_hours, row_ot_hours)
    gross = gross_total_norm_hour_total_ot_hour[0]
    total_norm_hour = gross_total_norm_hour_total_ot_hour[1]
    total_ot_hour = gross_total_norm_hour_total_ot_hour[2]

    #EXTRACTS MULTIPLE VALUES FROM THE RETURN OF CALCULATE_TAX
    tax_rate = (0.3, 0.4)[Employee_RoleID == 1]
    Sup_an_val_Helt_Ins_Tax_Net_Pay = Calculate_Tax(gross, tax_rate, Employee_Sup_an,
                                                                      Employee_Helt_Ins)
    Sup_an_val = Sup_an_val_Helt_Ins_Tax_Net_Pay[0]
    Tax = Sup_an_val_Helt_Ins_Tax_Net_Pay[2]
    Net_Pay = Sup_an_val_Helt_Ins_Tax_Net_Pay[3]

    #DISPLAY HOURS WORKED AND CALCULATIONS
    Internal_Processing.header("PAYSLIP")
    print("Hours you have worked:")
    for index in range(7):
        print('{0:20} {1:20} '.format(weekdays_short[index] + " Normal Hours", str(row_norm_hours[index])))
        print('{0:20} {1:20} '.format(weekdays_short[index] + " Overtime Hours", str(row_ot_hours[index])))
    print()
    print('{0:20} {1:20} '.format("Gross: ", locale.currency(gross)))
    print('{0:20} {1:20} '.format("Superannuation %:",str(Employee_Sup_an)+ "%"))
    print('{0:20} {1:20} '.format("Super. Deduct.:", locale.currency(Sup_an_val)))
    print('{0:20} {1:20} '.format("Health Insurance",locale.currency(Employee_Helt_Ins)))
    print('{0:20} {1:20} '.format("Tax rate%: ", str(tax_rate*100)+ "%"))
    print('{0:20} {1:20} '.format("Tax payed: ", locale.currency(Tax)))
    print('{0:20} {1:20} '.format("Net pay: ",locale.currency(Net_Pay)))

    #table print FORMAT

    display(Employee_ID)
#OBSOLETE IN NEW SYSTEM - USES INPUT OF NUMBER OF HOURS
#def Calculate_Wage_One_Person(Employee_ID):
#choices = {}
#choices[0] = "Yes"
#choices[1] = "No"
#firstShift = False
#while True:
#    input_choice=1
#    sql = "SELECT * FROM Employee WHERE ID=" + Employee_ID
#    cursor.execute(sql)
#    row = cursor.fetchall()

#    if len(row):
#        Employee_ID = row[0][0]
#        Employee_Fname = row[0][1]
#        Employee_Lname = row[0][2]
#        Employee_RoleID = row[0][3]
#        Employee_Sup_an = row[0][4]
#        Employee_Helt_Ins = row[0][5]

#        break
#    else:
#        print("Employee Cannot be found")

#        input_choice = Internal_Processing.select(choices, "Try again?")
#        if input_choice == 1:  # No
#            print("Going Back to subMenu - Add/Edit/View Employee")
#            Internal_Processing.display_submenu_AE_EmpDet()
##INPUT HOURS
#print("Hi ", Employee_Fname)
#print()


#weekdays = {}
#weekdays[0] = "Monday"
#weekdays[1] = "Tuesday"
#weekdays[2] = "Wednesday"
#weekdays[3] = "Thursday"
#weekdays[4] = "Friday"
#weekdays[5] = "Saturday"
#weekdays[6] = "Sunday"

#weekhours= {}
#weekhoursDB = {}
#weekhoursOT = {}
##OLD SYSTEM - INPUTTING HOURS
###ql = "SELECT * FROM Schedule WHERE EmployeeID=" + str(Employee_ID)
##ursor.execute(sql)
##ow = cursor.fetchall()
##f len(row) != 0:
##   for iterator in range(2,9):
##       weekhoursDB[iterator - 2] = row[0][iterator]
##lse:
##   for iterator in range(7):
##       weekhoursDB[iterator] = "0"
##       firstShift = True


##hile True:
##   print("Please input yours hours for each day below: (Leave Blank, if the default is your hours)")
##   for iterator in range(7):
##       while True:
##           weekhours[iterator] = input(weekdays[iterator] + "(Default: " + str(weekhoursDB[iterator]) +" ):")
##           if  weekhours[iterator]!="" and Internal_Processing.str_to_float_verify(weekhours[iterator]):
##               if float(weekhours[iterator]) > 20 or float(weekhours[iterator])<0:
##                   print("Please input a valid hour")

##               else:
##                   weekhoursDB [iterator] = float(weekhours[iterator])
##                   break
##           elif weekhours[iterator]=="":
##               break
##           elif weekhours[iterator]!="": #when str_to_float_verify is false
##               print("Please input a numerical entry")

##   print()
##   print("Please Confirm the details below:")
##   for iterator in range(7):
##       print(weekdays[iterator] + ": " + str(weekhoursDB[iterator]))

##   Confirmation = Internal_Processing.select(choices,
##                         "Are the Details correct? (Select from the choices)")  # Confirrmation of Data
##   if Confirmation == 0:  # Yes

##       break
##   if Confirmation == 1:  # No
##       input_choice = Internal_Processing.select(choices, "Try again?")
##       if input_choice == 1:  # No
##           print("Going Back to Menu")
##           Internal_Processing.display_menu()

##UPDATE DATABASE / INSERT NEW SCHEDULE
#if firstShift == True:
#    sql = "INSERT INTO Calculation(EmployeeID,MonH,TueH,WedH,ThuH,FriH,SatH,SunH,MonOH,TueOH,WedOH,ThuOH,FriOH,SatOH,SunOH) VALUES('" + str(
#        Employee_ID)

#    for index in range(7):
#        sql = sql + "','" + str(weekhoursDB[index])

#    for index in range(7):
#        sql = sql + "," + str(weekhoursOT[index])

#    sql = sql + "');"
#    cursor.execute(sql)
#    cursor.commit()  # CONFIRMS INSERT

#elif firstShift == False:
#    weekdays_short = {}
#    weekdays_short[0] = "Mon"
#    weekdays_short[1] = "Tue"
#    weekdays_short[2] = "Wed"
#    weekdays_short[3] = "Thu"
#    weekdays_short[4] = "Fri"
#    weekdays_short[5] = "Sat"
#    weekdays_short[6] = "Sun"

# # sql = "UPDATE Calculation SET MonH=" + str(weekhoursDB[0]) + ", TueH=" + str(weekhoursDB[1]) + ", WedH=" + str(
# #     weekhoursDB[2])+ ", ThuH=" + str(weekhoursDB[3]) + ", FriH=" + str(weekhoursDB[4]) \
# #       + ", SatH=" + str(weekhoursDB[5]) + ", SunH=" + str(weekhoursDB[6]) + " WHERE EmployeeID=" + str(Employee_ID)#
#
#    sql = "UPDATE Calculation SET "

#    for index in range(7):
#        sql += weekdays_short[index] + "H'" + str(weekhoursDB[index]) + ", "

#    for index in range(6):
#        sql += weekdays_short[index] + "OH'" + str(weekhoursDB[index]) + ", "

#    sql += weekdays_short[6] + "OH'" + str(weekhoursDB[6]) + " WHERE EmployeeID=" +str(Employee_ID)



#    cursor.execute(sql)
#    cursor.commit()

#    #SHOW CALCULATIONS OF TAXES AND GROSSPAY
#tax_rate = (0.3,0.4)[Employee_RoleID==1]
#Calculate_Tax(GrossPay(Employee_RoleID,weekhoursDB),tax_rate,Employee_Sup_an,Employee_Helt_Ins)

#print("Going back to MENU")
#print()
#print()
##Internal_Processing.display_menu()


def GrossPay(role,weekhours,weekhours_overtime): #CALCULATES GROSS PAY
   total_norm_hour = 0
   total_ot_hour = 0
   gross = 0
   pay_rate = (23.0,30.0)[role==1] #role: 2 - Barista, 1 - Manager
   pay_day = 0

   if len(weekhours) != 7:
       return "Number of Weekday is 7 -> 7 Input is required"

   for index in range(0,7): # count = 0 to 6
       norm_hour = weekhours[index]
       ot_hour = weekhours_overtime[index]

       total_norm_hour += norm_hour
       total_ot_hour += ot_hour


       if index<5: #WEEKDAYS
           if ot_hour>3:
               ot_hour = (ot_hour-3)   #pay = (pay_rate * hours) * % increase  Hence: pay = (hours * %increase) * pay_rate
               pay_day +=  pay_rate * ot_hour * 1.45                 #calculation of hours increase relative to normal hours
               ot_hour = 3

           pay_day = pay_rate * (norm_hour + ot_hour*1.25)

       else:       #WEEKENDS
           pay_day = (pay_rate+(3,4)[index==6])*(ot_hour*1.5+norm_hour)  #index = 5 or 6; $3 for SAT, $ $4 for SUN
       #print(str(index) + ": " + str(pay_day))
       gross = gross + pay_day



   return gross,total_norm_hour,total_ot_hour #MULTIPLE RETURN VALUE

def input_range_int(start,end,message): #CHECKS THE RANGE OF INPUT TO LIMIT INTO INTEGER
    #USED FOR LIMITTING INPUT OF CLOCKS
    print(message)
    while True:
        input_str = input("Entry: ")
        if Internal_Processing.str_to_int_verify(input_str)==True:
            input_int = int(input_str)
            if start <= input_int and input_int <= end:
                break
            else:
                print("Entry is not in available range")
        else:
            print("Entry is not an integer")

    return input_int


def time_array_to_hour(time_array): #CONVERTS TIME ARRAY/TUPLE TO HOUR
    def get_hour(time_str):
        h, m, s = time_str.split(':')
        return int(h) + int(m) / 60.0 + int(s) / 3600.0  # returns as double

    date_str = time.strftime("%H:%M:%S", time_array)
    hour = get_hour(date_str)
    return hour

def hour_am_pm(hour): #ASKS WHETHER ITS AN AM OR PM AND THEN CONVERTS TO 24 HOUR CONVENTION OF CLOCK (MILITARY CONVENTION)
    choices = {}
    choices[0] = "am"
    choices[1] = "pm"
    choice=Internal_Processing.select(choices,"Is it an am or pm?")

    if choice == 1: #pm
        hour = hour + 12
        if hour == 24:
            hour = 12
    elif hour == 12: #12 am
        hour = 0

    return hour

def int_to_time_array(year,month,day,hour,minute,second): #COMPILES SET OF INTEGERS(DATE) INTO TIME ARRAY
    time_array = (year, month, day, hour, minute, second, day-1, 317, 0) #3 last numbers are format or UNKNOWN
    return time_array

def time_array_to_string_db(time_array): #CONVERTS TIME ARRAY TO SUITABLE SAVING STRING FORMAT
    date_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return date_str

def time_array_to_string_print(time_array):
    #CONVERTS TIME ARRAY TO PRINTABLE STRING FORMAT [DO NOT STORE THIS VALUE BECAUSE THERE IS NO DATE IN THIS]
    #NO YEAR, MONTH, DAY
    date_str = time.strftime("%a %I:%M:%S %p", time_array)
    return date_str

def time_array_to_string_print_delta(time_array): #PRINTS TIME ARRAY AS A STRING FORMAT SUITABLE FOR ONLY HOURS
    date_str = time.strftime(" %H:%M:%S", time_array)
    return date_str

def string_to_time_array(date_str): #CONVERTS TIME STRING TO A TIME ARRAY/TUPLE
    time_array = time.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return time_array[0:9]

def time_subtraction(start,end): #TIME SUBTRACTION

    def days_hours_minutes_second(delta): #CONVERTS CHANGE IN TIME INTO ARRAY
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds // 60) % 60
        seconds = delta.seconds % 60
        return 2018,1,days,hours,minutes,seconds,2, 317, 0

    FMT = '%Y-%m-%d %H:%M:%S' #FORMAT OF TIME SUBTRACTION
    t1 = time.strftime(FMT, start) #MY FIRST TIME
    t2 = time.strftime(FMT, end)   #MY SECOND TIME

    tdelta = dt.strptime(t2, FMT) - dt.strptime(t1, FMT) #CHANGE IN TIME  - CAN ONLY BE DONE STRING FORMAT
    tdelta_tuple = days_hours_minutes_second(tdelta) #SPECIAL STRING FORMAT TO ARRAY
    return tdelta_tuple #RETURNS VALUE AS AN ARRAY/TUPLE


def Calculate_Tax(GrossPay, tax_rate, Sup_an, Helt_Ins): #CALCULATES DEDUCTIONS AND TAX
   Sup_an_val = GrossPay *(Sup_an / 100.0) #CALCULATES VALUE OF SUPERANNUATION DEDUCTION
   Wage_w_deduction = GrossPay - Sup_an_val - Helt_Ins #TAKES THE WAGE WITH DEDUCTION
   Tax = tax_rate*(Wage_w_deduction) #TAXATION CALCULATION

   Net_Pay = Wage_w_deduction - Tax #NET PAY

   return Sup_an_val,Helt_Ins,Tax,Net_Pay #RETURNS MULTIPLE VALUES


def input_date_time(EmployeeID):
    #INPUT TIME

    choices={}
    choices[0]= "Monday"
    choices[1] = "Tuesday"
    choices[2] = "Wednesday"
    choices[3] = "Thursday"
    choices[4] = "Friday"
    choices[5] = "Saturday"
    choices[6] = "Sunday"

    while True:

        year = 2018
        month = 1 # January 1,2018 is MONDAY : time subtraction will be easier
        global day #to be used later on
        day = Internal_Processing.select(choices,"Select which day:")+ 1 #MONDAY STARTS WITH 1 BY CONVENTION OF DAYS
        hour =input_range_int(1,12,"Please input the hour(HH) ")
        minute = input_range_int(0,59,"Please input the minute(MM)")
        second = 0
        #second = input_range_int(0,59,"Please input the second(SS) ")
        hour = hour_am_pm(hour)

        time_array = int_to_time_array(year,month,day,hour,minute,second)
        print("Please Confirm the Date/Time entered below from the format HH:MM:SS")
        print(time_array_to_string_print(time_array))

        Yes_No_choices = {}
        Yes_No_choices[0] = "Yes"
        Yes_No_choices[1] = "No"

        Confirmation = Internal_Processing.select(Yes_No_choices,
                              "Are the Details correct? (Select from the choices)")  # Confirrmation of Data
        if Confirmation == 0:  # Yes
            break
        if Confirmation == 1:  # No
            input_choice = Internal_Processing.select(Yes_No_choices, "Try again?")
            if input_choice == 1:  # No
                print("Going Back to Menu")
                display(EmployeeID)


    return time_array

def clock_in(EmployeeID): #CLOCK IN SECTION
    #EmployeeID = 2447532

    sql = "UPDATE Schedule SET "
    day_selection = {}
    day_selection[0] = "Mon"
    day_selection[1] = "Tue"
    day_selection[2] = "Wed"
    day_selection[3] = "Thu"
    day_selection[4] = "Fri"
    day_selection[5] = "Sat"
    day_selection[6] = "Sun"

    time_clock_in = input_date_time(EmployeeID)
    sql = sql + day_selection[day-1] +"DateIn ='" + time_array_to_string_db(time_clock_in) + "' WHERE EmployeeID = " + str(EmployeeID)
    #print(sql)
    cursor.execute(sql)
    cursor.commit()
    print("Clock-In Successful")
    print("Going back to Submenu - Employees")
    display(EmployeeID)

def clock_out(EmployeeID): #CLOCK OUTS AND CALCULATES AND UPDATES THE CALCULATION TABLE
    # 0 - ScheduleID
    # 1 - EmployeeID
    # 2 - Mon - 9
    # 3 - Tue - 10
    # 4 - Wed - 11
    # 5 - Thu - 12
    # 6 - Fri - 13
    # 7 - Sat - 14
    # 8 - Sun -15
    # ClockOut_Index - ClockIn_Index = 7
    # if overnight -> delta(Clockout) = 8

    # ClockIn_Index = Day# + 1 Eg. Mon + 1 = 2
    # Clockout_Index = Day# + 8 Eg. Mon + 8 = 9
    #EmployeeID = 2447532

    sql = "UPDATE Schedule SET "
    day_selection = {}
    day_selection[0] = "Mon"
    day_selection[1] = "Tue"
    day_selection[2] = "Wed"
    day_selection[3] = "Thu"
    day_selection[4] = "Fri"
    day_selection[5] = "Sat"
    day_selection[6] = "Sun"

    time_clock_out = input_date_time(EmployeeID)


    sql = sql + day_selection[day - 1] + "DateOut ='" + time_array_to_string_db(
        time_clock_out) + "' WHERE EmployeeID = " + str(EmployeeID) #STRING ADDITION OF SQL

    Clockout_index = day + 8
    sql_select = "SELECT * FROM Schedule WHERE EmployeeID=" + str(EmployeeID) + ""
    cursor.execute(sql_select)

    today_index = Clockout_index - 7
    yesterday_index = Clockout_index - 8
    if (Clockout_index== 9): # Monday, Clock-in on Sunday
        IsMonday=True
        yesterday_index = 8

    for row in cursor.fetchall():
        today_in = str(row[today_index])
        yesterday_in =str(row[yesterday_index])

   #print("Todayin: ",today_in)
   #print("yesterday: ", yesterday_in)
   #print(time_array_to_string_db(time_clock_out))
    if today_in=="None" and yesterday_in== "None": #NO AVAILABLE CLOCK IN SO NO CLOCK OUT
        print("No Clockout Available for that day ")
        print("Cancelling Clockout")
        print("Going back to menu ")
        display(EmployeeID)

    delta_tuple = time_subtraction(string_to_time_array(today_in),time_clock_out) #TIME SUBTRACTION FUNCTION
    if delta_tuple[3]<0 or delta_tuple[2]!=0: # negative hour -> OVERNIGHT
        if today_in == "None" or yesterday_in == "None": #CHECKS WHETHER ONE OF THEM IS EMPTY SINCE THE INVALID HOUR
            print("No Clockout Available for that day ")
            print("Cancelling Clockout")
            print("Going back to menu ")
            display(EmployeeID)
        else:
            delta_tuple = time_subtraction(string_to_time_array(yesterday_in), time_clock_out) #OVERNIGHT TIME CALCULATION
            IsOvernight = True

    if delta_tuple[2]!=0: #day interval
        print(delta_tuple)
        print("No Clockout Available for that day ")
        print("Cancelling Clockout")
        print("Going back to menu ")
        display(EmployeeID)

    print("Did you work this following time length: (Format HH:MM:SS):")
    print(time_array_to_string_print_delta(delta_tuple))

    Yes_No_choices = {}
    Yes_No_choices[0] = "Yes"
    Yes_No_choices[1] = "No"

    if Internal_Processing.select(Yes_No_choices,"Confirmation: ") == 0: #YES
        ##print(sql)
        cursor.execute(sql)
        cursor.commit()

       # print(time_array_to_hour(time_clock_out))

        today_hour = time_array_to_hour(time_clock_out) #HOUR EQUIVALENT OF TODAY
        today_othour = 0
        yesterday_hour = 0

        #6.5 - 15.5 normal hours
        today_in_hour = time_array_to_hour(string_to_time_array(today_in))


        if today_hour >15.5 and  today_in_hour<15.5:  #SCENARIO: A:N - NORMAL HOURS + OVERNIGHT
            today_othour =  today_hour - 15.5
            today_hour = 15.5 - today_in_hour

        elif today_hour >15.5 and  today_in_hour>15.5: #Scenario N:N - ALL OVERNIGHT
            today_othour =  today_hour - today_in_hour
            today_hour = 0 #convert all to OVERTIME
        else: #SCENARIO A:A - ALL NORMAL HOURS
            today_hour = today_hour - today_in_hour

        #SAVES HOURS VIA INDEX-1 FOR ARRAY CONVENTION
        sql = "UPDATE Calculation Set "
        sql = sql + day_selection[day - 1] + "H ='" + str(today_hour) + "', " + day_selection[day - 1] + "OH ='"+ str(today_othour) +"' WHERE EmployeeID = " + str(EmployeeID)
        #print(sql)
        cursor.execute(sql)
        cursor.commit()

        print("Clock-Out Successful")
        print("Going back to Submenu - Employees")
        display(EmployeeID)

    else:
        print("Cancelling Clockout")
        print("Going back to menu ")
        display(EmployeeID)








