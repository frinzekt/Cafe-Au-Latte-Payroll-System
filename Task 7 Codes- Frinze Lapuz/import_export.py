# Import_export.py
# this file is responsible in importing and exporting data
#
# Name: Frinze Lapuz

import pyodbc #db
import inspect#inspecting files
import os     #os manipulation
import os.path#directories path
import random #random number generator
import sys    #cmd access (windows cmd in the future)
import locale #currency
import numpy as np #array manipulation

import Internal_Processing
import wage_calculations

#EXCLUSIVE
import csv #uses csvwriter and csvreader

locale.setlocale(locale.LC_ALL,'') #sets format of currency $xx.xx

conn=r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\CAL_DB.accdb;' #PATHNAME
conn = pyodbc.connect(conn)  #DB Connector
cursor = conn.cursor() #Table Adapter / DB Cursor

def Imp_data_from_csv(): #Imports data from csv
    global entry_num #Entry number of importing
    global outcome #error checking of 0 or -1
    outcome =0
    entry_num = 0

    choices = ["Yes","No"] #using Internal_processing.select()
    while True: #DO-WHILE EQUIVALENT
        filename = input("Please input the filename in the format FILENAME.csv replacing 'FILENAME' into the name of the file (CASE SENSITIVE): ")
        filename = str(filename) +".csv"
        if os.path.isfile(filename): #checks if file exist
            break
        else:
            print("'",filename,"' File cannot be found")
            choice = Internal_Processing.select(choices,"Try again:")
            if choice == 1: #NO
                print("Import Failed Going Back to previous menu")
                Internal_Processing.display_submenu_AE_EmpDet()

    #HeaderList is the list of requirements of the program
    HeaderList = {}
    HeaderList[0] ="First Name"
    HeaderList[1] ="Last Name"
    HeaderList[2] ="Role"
    HeaderList[3] ="Superannuation"
    HeaderList[4] ="Health Insurance"
    HeaderList[5] ="Monday Hours"
    HeaderList[6] ="Tuesday Hours"
    HeaderList[7] ="Wednesday Hours"
    HeaderList[8] = "Thursday Hours"
    HeaderList[9] = "Friday Hours"
    HeaderList[10] = "Saturday Hours"
    HeaderList[11] = "Sunday Hours"
    HeaderList_Length = len(HeaderList)


    CSVHeaderList = {}
    print("Please input the equivalent header in your csv file for the following(CASE SENSITIVE):")
    for index in range(HeaderList_Length): #CSVHeaderList will include the equivalent header
        CSVHeaderList[index] = input(str(HeaderList[index]) + ": ")

    bool_check_headers = True

    with open(filename) as csvfile: #Open as a dictionary reader
        reader = csv.DictReader(csvfile)

        for row in reader:
            if bool_check_headers:
                CONTINUE=check_headers_exist(row,CSVHeaderList,HeaderList_Length,HeaderList)
                if CONTINUE == False: #When error arises, this runs in headers name
                    print("IMPORT FAILED")
                    print("Going back to previous menu")
                    Internal_Processing.display_submenu_AE_EmpDet()

            entry_num = entry_num +1 #Contains which row is being processed

            try: #Try importing
                Employee_ID = import_to_table_employee(row[CSVHeaderList[0]],row[CSVHeaderList[1]],row[CSVHeaderList[2]],row[CSVHeaderList[3]],row[CSVHeaderList[4]])
            except ValueError or Employee_ID==-1 or KeyError: #Can result in a variety of error
                print("IMPORT FAILED <--> Employee LIST FOR ENTRY: ",entry_num)
            else:#ONLY DO THIS IF EXCEPT DOESNT WORK
                try:
                    outcome=import_to_table_schedule(Employee_ID,row[CSVHeaderList[5]],row[CSVHeaderList[6]],row[CSVHeaderList[7]],row[CSVHeaderList[8]],row[CSVHeaderList[9]],row[CSVHeaderList[10]],row[CSVHeaderList[11]])
                except ValueError or outcome==-1:
                    print("IMPORT FAILED <--> Schedule LIST FOR ENTRY: ",entry_num)
    print()
    print("Returning to Submenu - For Managers/Administrators")
    Internal_Processing.display_submenu_AE_EmpDet()


def import_to_table_employee(Employee_Fname,Employee_Lname,Employee_Role,Employee_Sup_an,Employee_Helt_Ins):
#Inserts imports to DBtable
    if Employee_Role.lower()=="barista": #recognize role
        Employee_RoleID = 2
    elif Employee_Role.lower()=="manager":
        Employee_RoleID = 1
    else:
        print("IMPORT FAILED <--> Employee LIST FOR ENTRY: ", entry_num) #role unavailable
        return -1 #prevents the code from running further
    Employee_ID = generate_unique_random()


    sql = "INSERT INTO Employee (ID,FName,LName,RoleID,Sup_an,Helt_Ins) VALUES('" + str(
        Employee_ID) + "','" + Employee_Fname + "','" + Employee_Lname + "','" + str(Employee_RoleID) + "','" + str(
        Employee_Sup_an) + "','" + str(Employee_Helt_Ins) + "');"

    cursor.execute(sql) #SQL EXECUTE
    cursor.commit()

    return Employee_ID

def import_to_table_schedule(Employee_ID,Mon,Tue,Wed,Thu,Fri,Sat,Sun): #Insert Imports to DBtable
    weekhoursDB = [Mon,Tue,Wed,Thu,Fri,Sat,Sun]
    weekhoursOT = [0,0,0,0,0,0,0] #Initializee as all 0

    if Employee_ID==-1: #Does not execute if invalid EmployeeID / Refer to try and except of function calling this
        print("IMPORT FAILED <--> Calculation List FOR ENTRY: ",entry_num)
        return -1
    Isprinted = False
    length = len(weekhoursDB)
    for index in range(length):
        if  float(weekhoursDB[index])<24 and float(weekhoursDB[index])>=0: #Prevents import more than 24 and less 0
            if float(weekhoursDB[index])>9: #Eg. Weekhours = 15
                weekhoursOT[index] = float(weekhoursDB[index]) - 9 #Overtime = 6
                weekhoursDB[index] = 9 #Normal = 9 ; 9+6 = 15 HOORAY!
        else:
            if Isprinted == False:
                print("IMPORT FAILED <--> Hours more than 24 or less than 0 in a day <-> Replacing Invalid hours as 0 FOR ENTRY: ", entry_num)
                Isprinted = True
            weekhoursDB[index] = 0 #saves as 0 for when hours more than 24

    sql = "INSERT INTO Schedule (EmployeeID) VALUES('" + str(Employee_ID) + "');"
    cursor.execute(sql)
    cursor.commit()  # CONFIRMS INSERT

    sql = "INSERT INTO Calculation(EmployeeID,MonH,TueH,WedH,ThuH,FriH,SatH,SunH,MonOH,TueOH,WedOH,ThuOH,FriOH,SatOH,SunOH) VALUES('" + str(
        Employee_ID)

    for index in range (length): #STRING ADDITTION OF NORMAL HOURS
        sql = sql + "','" + str(weekhoursDB[index])

    for index in range (length): #STRING ADDITION OF OVERTIME HOURS

        sql = sql + "','" + str(weekhoursOT[index])

    sql = sql + "');"

    #print(sql)
    cursor.execute(sql)
    cursor.commit()

    print("IMPORT SUCCESSFUL FOR ENTRY:",entry_num)


def check_headers_exist(row,CSVHeaders,length,HeaderList): #CHECK HEADERS IF IT EXIST
    for index in range(length):
         try:
             checker=row[CSVHeaders[index]] #ASSIGNING A VALUE TO A VARIABLE FOR WHICH VALUE DOES NOT EXIST IS ERROR
         except KeyError: #KEY ERROR IS THE PRIMARY ERROR OF TRYING TO SEARCH IN DICTIONARY A HEADER THAT DOES NOT EXIST
             print(CSVHeaders[index],"is not equivalent to",HeaderList[index])
             return 0
    return 1

def generate_unique_random():
    while True: #REPEATS GENERATING ID UNTIL IT BECOMES RANDOM
        Employee_ID = random.randint(1000000, 9999999)                      #Generates Random ID
        sql = "SELECT COUNT(*) FROM Employee WHERE ID=" + str(Employee_ID)  #CHECK WHETHER ID EXIST IN TABLE
        cursor.execute(sql)
        row = cursor.fetchall()                                             #cursor.fetchall() returns 2D array always
        if row[0][0] == 0:                                                  #Pin doesnt exist in database
            break;

    return Employee_ID

def export_payroll():
    #Concatenate 2 2D-array (y,x)
    #SUMMARY: DATA FROM 2 TABLES
    #TABLE1: CONTAINS EMPLOYEE DETAILS
    #TABLE2: CONTAINS SCHEDULE AND HOURS
    #TABLE2 NEEDS ADDITION OF CALCULATABLE FIELDS  THEN JOIN WITH TABLE 1

    #https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-58.php

    sql_employee= "SELECT Employee.ID, Employee.FName, Employee.LName, Employee.RoleID, Role.TaxRate, Employee.Sup_an, Employee.Helt_Ins FROM Role INNER JOIN Employee ON Role.RoleID = Employee.RoleID;"
    cursor.execute(sql_employee) #Column 0 - 5
    row_employee = cursor.fetchall()


    num_rows = len(row_employee)
    num_cols = len(row_employee[0])


    row_calculation_complete = np.chararray((num_rows,14),itemsize=10) #CREATES AN 2D ARRAY THAT CAN STORE 10 CHARACTERS FOR EACH ELEMENT
    row_calculation_complete.fill("") #INITIALIZE

    row_tax_rate = np.chararray((num_rows,1),itemsize=10) #TAX RATE IS DISJOINTED FROM THE 2 TABLE SO NEED TO CREATE A 2D ARRAY THAT ONLY HAS 1 COLUMN
    row_tax_rate.fill("")                                 #2D ARRAY IS SO THAT IT IS COMPATIBLE FOR CONCATENATION



#
    #final employee = ["ID","GNAME","SNAME","ROLE","TRATE","SUPER","HLTH"]
    #current employee = ["ID","GNAME","SNAME","ROLE","SUPER","HLTH"]          TRATE MISSING
    #final calculations = [MON,TUE,WED,THU,FRI,SAT,SUN,NHRS,OHRS,GROSS,SDED,HDED,TAX,NETT]
    #calculation = [GrossPay,Sup_an_val,Helt_Ins,Tax,Net_Pay]

    for index in range(num_rows): #dealing witb changing rows

        Employee_RoleID = row_employee[index][3] #EXTRACTION OF EMPLOYEE ROLE ID
        row_employee[index][3] = ["Manager","Barista"][Employee_RoleID==2] #ROLEID TO ROLE NAME

        Employee_Tax_rate = row_employee[index][4] #EXTRACTION OF TAX RATE
        row_employee[index][4] = str(Employee_Tax_rate) + "%"

        Employee_Sup_an = row_employee[index][5] #EXTRACTION OF SUPERANNUATION PERCENTAGE
        row_employee[index][5] = str(Employee_Sup_an)+"%" #ADDING PERCENT SIGN

        Employee_Helt_Ins = row_employee[index][6] #EXTRACTION OF HEALTH INSURANCE
        row_employee[index][6] = locale.currency(Employee_Helt_Ins) #FORMATTING $XX.XX


        sql_calcultion = "SELECT MonH,TueH,WedH,ThuH,FriH,SatH,SunH,MonOH,TueOH,WedOH,ThuOH,FriOH,SatOH,SunOH FROM Calculation WHERE EmployeeID=" + str(row_employee[index][0]) #EmployeeID
        cursor.execute(sql_calcultion)
        row_calculation = cursor.fetchall() #one row only

        row_norm_hours = {}
        row_ot_hours = {}

        #print(sql_calcultion)
        #print(row_calculation)
        for col in range(7): #EXTRACTS THE VALUE OF TABLE2 INTO ARRAYS - NORM - OT HOURS
            row_norm_hours[col] = row_calculation[0][col]
            row_ot_hours[col] = row_calculation[0][col+7]


        #print("Row_norm_ho",row_norm_hours)
        #print("Row_ot_ho",row_ot_hours)
        gross_total_norm_hour_total_ot_hour = wage_calculations.GrossPay(Employee_RoleID,row_norm_hours,row_ot_hours)
        gross = gross_total_norm_hour_total_ot_hour[0] #EXTRACT RETURN DATA
        total_norm_hour = gross_total_norm_hour_total_ot_hour[1]
        total_ot_hour = gross_total_norm_hour_total_ot_hour[2]

        tax_rate = (0.3, 0.4)[Employee_RoleID == 1]
        Sup_an_val_Helt_Ins_Tax_Net_Pay = wage_calculations.Calculate_Tax(gross,tax_rate,Employee_Sup_an,Employee_Helt_Ins)
        Sup_an_val = Sup_an_val_Helt_Ins_Tax_Net_Pay[0] #EXTRACT RETURN DATA
        Tax = Sup_an_val_Helt_Ins_Tax_Net_Pay[2]
        Net_Pay = Sup_an_val_Helt_Ins_Tax_Net_Pay[3]



        for index_col in range(7): #PUT DIFFERENT NAME FOR LOOP SO NOT TO AFFECT OTHER LOOPS (SOME RANDOM BUG?)
            row_calculation_complete[index][index_col] = str(row_norm_hours[index_col] +row_ot_hours[index_col])

        #FORMATTING OF EXPORT
        row_calculation_complete[index][7] = total_norm_hour
        row_calculation_complete[index][8] = total_ot_hour
        row_calculation_complete[index][9] = locale.currency(gross)
        row_calculation_complete[index][10]= locale.currency(Sup_an_val)
        row_calculation_complete[index][11]=locale.currency(Employee_Helt_Ins)
        row_calculation_complete[index][12]=locale.currency(Tax)
        row_calculation_complete[index][13]=locale.currency(Net_Pay)

        #print("ROW CALC COMPLTETE", row_calculation_complete)


    a = np.array(row_employee) #TEMPORARY ARRAY FOR JOINING 1 : EMPLOYEE DATA
    b = np.array(row_calculation_complete) #TEMPORARY FOR JOINING 2 : HOURS AND CALCULATABLE FIELDS
    row_multiple  = np.concatenate((a,b),1) #THE FINAL 2D ARRAY
    #print (row_multiple)

    #HEADER FORMAT OF ARRAY
    headers =["ID","GNAME","SNAME","ROLE","TRATE","SUPER","HLTH","MON","TUE","WED","THU","FRI","SAT","SUN","NHRS","OHRS","GROSS","SDED","HDED","TAX","NETT"]
    with open("payroll.csv", "w+") as myFile:
        csvWriter = csv.writer(myFile,delimiter=',')
        csvWriter.writerow(headers) #ACCEPTS 1D ARRAY
        csvWriter.writerows(row_multiple)#ACCEPTS 2D ARRAY AND TURN IT INTO CSV

    print("Export to payroll.csv is successful")
    print()
    print("Returning to Submenu - For Managers/Administrators")
    Internal_Processing.display_submenu_AE_EmpDet()

















