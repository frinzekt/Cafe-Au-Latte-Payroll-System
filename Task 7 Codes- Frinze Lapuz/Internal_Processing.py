#Internal Processing
#  This file is responsible for most of the nitpicking/error checking methods and also display menu
#
# Name: Frinze Lapuz


import pyodbc #db
import inspect
import os     #os manipulation, directories path
import random #random number generator
import sys    #cmd access (windows cmd in the future)
import locale #currency
import re     #alphanumeric limitation

import import_export
import wage_calculations

#set currency Dollars
locale.setlocale(locale.LC_ALL,'')

conn=r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\CAL_DB.accdb;' #PATHNAME
conn = pyodbc.connect(conn)  #DB Connector
cursor = conn.cursor() #Table Adapter / DB Cursor

def header(title): #PRINTS A NICE HEADER WITH THE TITLE

    print()
    print()
    print("----------------------------  " + str(title) + "  ----------------------------")

def authent_manager(): #AUTHENTICATES MANAGER
    tries = 3
    choices = {}
    choices[0] = "Yes"
    choices[1] = "No"

    while True:
        input_choice=1 #No
        while True:
            Employee_ID = input("Please Input Manager Employee ID (" + str(tries) +" remaining): ")
            if str_to_int_verify(Employee_ID) == True: #LIMITS VALUE TO INT
                break
            else:
                print("Please input an integer")

        sql = "SELECT * FROM Employee WHERE RoleID=1 AND ID=" + Employee_ID #RoleID=1 is Manager
        cursor.execute(sql)
        row = cursor.fetchall()

        if len(row): #row is more than 1 | in this case of unique ID, len(row) = 1
            break
        else:
            print("ManagerID Cannot be found") #no row
            tries -= 1
            if tries ==0:  # No
                return 0

            input_choice = select(choices, "Try again?")
            if input_choice == 1:  # No
                return 0
    return 1
def authent_employee(): #AUTHENTICATE EMPLOYEE
    tries = 3
    choices = {}
    choices[0] = "Yes"
    choices[1] = "No"

    while True: #DO WHILE LOOP
        input_choice = 1  # No
        while True:
            Employee_ID = input("Please Input Employee ID (" + str(tries) + " remaining): ")
            if str_to_int_verify(Employee_ID) == True: #LIMITS TO INT
                break
            else:
                print("Please input an integer")

        sql = "SELECT * FROM Employee WHERE ID=" + Employee_ID
        cursor.execute(sql)
        row = cursor.fetchall()

        if len(row):
            break
        else:
            print("Employee Cannot be found")
            tries -= 1
            if tries == 0:  # No
                return 0,Employee_ID

            input_choice = select(choices, "Try again?")
            if input_choice == 1:  # No
                return 0,Employee_ID
    return 1,Employee_ID #Returns either 1 or 0 as a BOOLEAN IF AUTHENTICATION IS CORRECT, #Returns EmployeeID for future reference

def generate_unique_random(): #GENERATE RANDOM UNIQUE NUMBER - LOCAL
    while True: #DO WHILE
        Employee_ID = random.randint(1000000, 9999999)                      #Generates Random Unique ID
        sql = "SELECT COUNT(*) FROM Employee WHERE ID=" + str(Employee_ID)
        cursor.execute(sql)
        row = cursor.fetchall()
        if row[0][0] == 0:                                                  #Pin doesnt exist in database
            break;

    return Employee_ID #RETURNS THE UNIQUE RANDOM NUMBER


def str_to_int_verify(string): #TRIES WHETHER STR COULD BE CONVERTED TO INT
    try:
        int(string)
        return True
    except ValueError:
        return False #RETURNS TRUE OR FALSE

def str_to_float_verify(string): #TRIES WHETHER STR COULD CONVERTED TO FLOAT
    try:
        float(string)
        return True
    except ValueError:
        return False #RETURNS TRUE OR FALSE

def select(choices_arr, Message): #LIMITS THE INPUT FROM CHOICES
    # ONE OF THE MOST USED FUNCTION
    # ACCEPTS A ARRAY FULL OF CHOICES
    # DISPLAYS MESSAGE (LIKE A PRINT STATEMENT AT THE BEGINNING)
    # RETURNS THE INDEX OF THE SELECTED CHOICE

    choices_arr_len = len(choices_arr)#

    print(Message)
    for i in range(len(choices_arr)): #PRINTS THE CHOICES
        print(str(i+1) + ". " + choices_arr[i]) #listing of the choices

    while True:
        print()
        choice_inputS = input("Choice: ")


        if str_to_int_verify(choice_inputS): #INPUT SHOULD BE AN INTEGER
            choice_input = int(choice_inputS)
            if choice_input>=1 and choice_input <= choices_arr_len: #test if the choice input is within the choices
                break #breaks out of the loop
            else:
                print("Error: input should be in the choices")
                print("You have inputted: "+ choice_inputS)
        else:
            print("Error: input should be an integer")
            print("You have inputted: " + choice_inputS)

    return (choice_input-1) #RETURNS INDEX FROM CHOICE

def input_limit_alphabet(prompt): #LIMITS INPUT TO ALPHABET

    while True: #ONLY ALLOW A-Z Characters
        input_str = input(prompt)
        input_str = input_str.lower() #turn every character to small caps
        if not re.match("^[a-z]*$", input_str): #test in range of small caps alphabet
            print("Error! Only letters a-z allowed!")
        else:
            break

    return input_str.title() #Capitalize first letter

def Ins_Employee(): #INSERT NEW EMPLOYEE
    roles = ["Mananger","Barrista"] #CHOICES OF ROLES
    sup_an_display = ["4% of wage","6% of wage","8% of wage","Choose Later"]
    sup_an_val = [4,6,8,0] #CHOICES OF SUPERANNUATION
    helt_ins_display = ["Ancillary: $15.00 per week","Standard: $25.00 per week","Superior: $45.00 per week","Choose Later"]
    helt_ins_val = [15,25,45,0] #CHOICES OF HEALTH INSURANCE
    Employee_Fname = input_limit_alphabet("Enter Employee First Name: ")
    Employee_Lname = input_limit_alphabet("Enter Employee Last Name: ")
    Employee_RoleID = select(roles,"Select the role of the employee from the choices by entering the number of the choice:")+1 #RETURN WITH ROLE INDEX, YET ROLES ID STARTS AT 1

    Employee_Sup_an = sup_an_val[select(sup_an_display,"Select the superanuation percentage from the choices by entering the number of the choice:")]
    Employee_Helt_Ins = helt_ins_val[select(helt_ins_display,"Select the ammount of health insurance payed per week from the choices by entering the number of the choice:")]

    print()
    print("Please Confirm the Details below:")
    print("Employee First Name:", Employee_Fname)
    print("Employee Last Name:", Employee_Lname)
    print("Employee Role:", roles[Employee_RoleID-1])
    print("Employee Superannuation(%):",Employee_Sup_an)
    print("Employee Health Insurance(per week):",Employee_Helt_Ins)
    Confirmation = select(["Yes","No"], "Are the Details correct? (Select from the choices)")#Confirrmation of Data

    if Confirmation ==1 :
        print("You have selected 'No', Going back to sub-menu 'Add New Employee'")
        display_submenu_AE_EmpDet()

    Employee_ID = generate_unique_random() #PRIMARY

    sql = "INSERT INTO Employee (ID,FName,LName,RoleID,Sup_an,Helt_Ins) VALUES('" + str(Employee_ID) + "','" + Employee_Fname + "','" + Employee_Lname + "','" + str(Employee_RoleID) + "','" + str(Employee_Sup_an) + "','" + str(Employee_Helt_Ins) + "');"
    try:
        cursor.execute(sql)
        cursor.commit()#CONFIRMS INSERT
    except ValueError:
        print("Error: SQL details please check")
        return 0

    #INSERT EMPTY TIME SHEET
    sql = "INSERT INTO Schedule (EmployeeID) VALUES('"+ str(Employee_ID) + "');"
    cursor.execute(sql)
    cursor.commit()  # CONFIRMS INSERT

    #INSERT EMPTY CALCULATION SHEET

    sql = "INSERT INTO Calculation (EmployeeID) VALUES('" + str(Employee_ID) + "');"
    cursor.execute(sql)
    cursor.commit()  # CONFIRMS INSERT


    print("Details are added:")
    print("Employee ID: ",Employee_ID)
    print("Employee First Name:", Employee_Fname)
    print("Employee Last Name:", Employee_Lname)
    print("Employee Role:", roles[Employee_RoleID - 1])

    display_submenu_AE_EmpDet()

def Edi_Employee(): #EDIT EMPLOYEE
    choices = {}
    choices[0] = "Yes"
    choices[1] = "No"

    while True:
        input_choice = 1  # Default is no for all choices
        while True:
            Employee_ID = input("Please Input Employee ID: ")
            if str_to_int_verify(Employee_ID) == True:
                break
            else:
                print("Please input an integer")

        sql = "SELECT * FROM Employee WHERE ID=" + Employee_ID
        cursor.execute(sql)
        row = cursor.fetchall()
        print()
        if len(row): #EXECUTES IF EMPLOYEE EXISTS
            cursor.execute(sql)
            print("Is this the Employee you want to be edited?")
            print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format("EmployeeID", "First Name", "Last Name", "Role",
                                                                       "Superannuation(%)",
                                                                       "Health Insurance($ per week)"))
            for row in cursor.fetchall(): #EXTRACTION OF DATA FROM SQL
                Employee_ID = row[0]
                Employee_Fname = row[1]
                Employee_Lname = row[2]
                Employee_RoleID = row[3]
                Employee_Sup_an = row[4]
                Employee_Helt_Ins = row[5]

                row[3] = ("Manager", "Barista")[row[3] == 2]
                Employee_Role = row[3]
                row[4] = str(row[4]) + "%"
                # row[4] =
                print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format(str(row[0]), row[1], row[2], row[3],
                                                                           str(row[4]),
                                                                           str(row[5])))
            input_choice = select(choices, "")
        else:
            print("Employee Cannot be found")

        if input_choice == 0:  # Yes
            break
        elif input_choice == 1:  # No
            input_choice = select(choices, "Try again?")
            if input_choice == 1:  # No
                print("Going Back to subMenu - Add/Edit/View Employee")
                display_submenu_AE_EmpDet()

    #EDIT EMPLOYEE IN PROGRAM ITSELF
    while True:
        print("Input New Values for each field [If there is no change to a field, leave it blank]")
        Fname = input_limit_alphabet("Enter First Name (Original: " + Employee_Fname + "): ")
        Lname = input_limit_alphabet("Enter Last Name (Original: " + Employee_Lname + "): ")

        role = {}
        role[0] = "Manager"
        role[1] = "Barista"

        sup_an_display = ["4% of wage", "6% of wage", "8% of wage", "Choose Later"] #CHOICES
        sup_an_val = [4, 6, 8, 0] #VALUES CORRESPONDING FROM THE CHOICES
        helt_ins_display = ["Ancillary: $15.00 per week", "Standard: $25.00 per week", "Superior: $45.00 per week",
                            "Choose Later"]
        helt_ins_val = [15, 25, 45, 0] #VALUES CORRESPONDIDNG FROM THE CHOICES

        Role = select(role,"Select Role (Original: " + Employee_Role + "): ") +1
        Employee_RoleID = Role
        if (Fname!=""):
            Employee_Fname = Fname
        if (Lname!=""):
            Employee_Lname = Lname

        if Employee_Sup_an == 0.: #CAN ONLY BB CHANGED ONCE
            Employee_Sup_an = sup_an_val[select(sup_an_display,
                                            "Select the superanuation percentage from the choices by entering the number of the choice(Original: " + str(Employee_Sup_an)+"%):")]
        if Employee_Helt_Ins==0:
            Employee_Helt_Ins = helt_ins_val[select(helt_ins_display,
                                                "Select the ammount of health insurance payed per week from the choices by entering the number of the choice(Original: " + str(Employee_Helt_Ins)+" per week):")]

        #CONFIRMATION OF INPUT
        print()
        print("Please Confirm the Details below:")
        print("Employee First Name:", Employee_Fname)
        print("Employee Last Name:", Employee_Lname)
        print("Employee Role:", role[Employee_RoleID-1])
        print("Employee Superannuation(%):", Employee_Sup_an)
        print("Employee Health Insurance(per week):", Employee_Helt_Ins)
        Confirmation = select(choices,
                              "Are the Details correct? (Select from the choices)")  # Confirrmation of Data
        if Confirmation == 0: #Yes
            break


        if Confirmation == 1: #No
            input_choice = select(choices, "Try again?")
            if input_choice == 1:  # No
                print("Going Back to subMenu - Add/Edit/View Employee")
                display_submenu_AE_EmpDet()

    #EDIT EMPLOYEE WITH SQL IN DATABASE
    sql = "UPDATE Employee SET Fname='" + Employee_Fname + "', Lname='" +Employee_Lname + "', RoleID='" +str(Employee_RoleID) +"', Sup_an='" +str(Employee_Sup_an) +"', Helt_Ins='" +str(Employee_Helt_Ins) + "' WHERE ID=" + str(Employee_ID)
    #print(sql)
    cursor.execute(sql)
    cursor.commit()

    print("EDIT SUCCESSFUL")
    print("Going Back to subMenu - Add/Edit/View Employee")
    display_submenu_AE_EmpDet()


def Del_Employee(): #DELETE EMPLOYEE
    choices = {}
    choices[0] = "Yes"
    choices[1] = "No"

    while True: #DO WHILE LOOP
        input_choice = 1 #Default is no for all choices
        while True:
            Employee_ID = input("Please Input Employee ID: ")
            if str_to_int_verify(Employee_ID) == True:
                break
            else:
                print("Please input an integer")

        #FINDING THE EMPLOYEE
        sql = "SELECT * FROM Employee WHERE ID=" + Employee_ID
        cursor.execute(sql)
        row = cursor.fetchall()
        print()
        if len(row):
            cursor.execute(sql)
            print("Is this the Employee you want to be deleted?")
            print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format("EmployeeID", "First Name", "Last Name", "Role",
                                                                       "Superannuation(%)", "Health Insurance($ per week)"))
            for row in cursor.fetchall():
                row[3] = ("Manager", "Barista")[row[3] == 2]
                row[4] = str(row[4]) + "%"
                # row[4] =
                print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format(str(row[0]), row[1], row[2], row[3], str(row[4]),
                                                                           str(row[5])))
            input_choice = select(choices, "")
        else:
            print("Employee Cannot be found")


        if input_choice == 0: #Yes
            break
        elif input_choice == 1: #No
            input_choice = select(choices,"Try again?")
            if input_choice == 1: #No
                print("Going Back to subMenu - Add/Edit/View Employee")
                display_submenu_AE_EmpDet()

    #DELETING ALL DEPENDENCIES
    sql = "DELETE FROM Calculation WHERE EmployeeID=" + str(Employee_ID)
    cursor.execute(sql)
    cursor.commit()

    sql = "DELETE FROM Schedule WHERE EmployeeID=" + str(Employee_ID)
    cursor.execute(sql)
    cursor.commit()

    #DELETE EMPLOYEE IF WHILE TRUE IS BROKEN(EXECUTES BREAK STATEMENT))
    sql = "DELETE FROM Employee WHERE ID=" + str(Employee_ID)
    cursor.execute(sql)
    cursor.commit()

    print("DELETE SUCCESSFUL")
    print("Going Back to subMenu - Add/Edit/View Employee")
    display_submenu_AE_EmpDet()


def display_menu(): #DISPLAY MAIN MENI
    header("MAIN MENU")
    choices = {}
    choices[0]="Add/Edit/View Employee Details"
    choices[1]="Employee Section"
    choices[2] ="Exit"
    input_choice = select(choices,"Select From the functionalities below:")

    if input_choice == 0: #FUNCTIONS CORRESPONDING ON CHOICES
        if (authent_manager()):
            display_submenu_AE_EmpDet()
        else:
            print("Invalid Authentication")
            display_menu()

    elif input_choice == 1:
        returns=authent_employee()
        Employee_ID = returns[1]
        if (returns[0]):
            wage_calculations.display(Employee_ID)
        else:
            print("Invalid Authentication")
            display_menu()
    elif input_choice == 2:
        sys.exit(0)


def DisplayEmployee(Willgobacktomenu): #DISPLAYS EMPLOYEE AND WILL GO BACK TO MENU IF SET TO 1
                                        #NEEDS 0 FOR EDIT AND DELETE EMPLOYEE
    header("EMPLOYEE LIST")
    sql = "select * from Employee ORDER BY Lname Asc "
    cursor.execute(sql)  # executes SQL from DB Cursor

    col = 5 - 1 #6 rows -1 = index
    print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format("EmployeeID", "First Name", "Last Name", "Role",
                                                               "Superannuation(%)", "Health Insurance($ per week)"))
    for row in cursor.fetchall():
        row[3] = ("Manager","Barista")[row[3]==2]
        row[4] = str(row[4]) + "%"
        #row[4] =
        print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format(str(row[0]),row[1],row[2],row[3],str(row[4]),str(row[5])))

    if (Willgobacktomenu == 1):
        display_submenu_AE_EmpDet()

def DisplayEmployee_byRole(Role):
    #DISPLAY EMPLOYEE BY ROLE
    header("EMPLOYEE LIST BY ROLE")
    sql = "select * from Employee WHERE RoleID=" + str(Role) + " ORDER BY Lname Asc " #DETERMINES THE ROLE SPECIFIED
   # print(sql)
    cursor.execute(sql)  # executes SQL from DB Cursor

    col = 5 - 1  # 6 rows -1 = index
    print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format("EmployeeID", "First Name", "Last Name", "Role",
                                                               "Superannuation(%)", "Health Insurance($ per week)"))
    for row in cursor.fetchall():
        row[3] = ("Manager", "Barista")[row[3] == 2]
        row[4] = str(row[4]) + "%"
        # row[4] =
        print('{0:20} {1:20} {2:20} {3:20}  {4:20}  {5:20}'.format(str(row[0]), row[1], row[2], row[3], str(row[4]),
                                                                   str(row[5])))

    display_submenu_AE_EmpDet()


def display_submenu_AE_EmpDet(): #DISPLAY SUBMENU
        header("SUB-MENU ADD/EDIT/VIEW EMPLOYEES")
        choices = {}

        choices[0] = "Display ALL Employees & Details"
        choices[1] = "Display ALL Managers & Details"
        choices[2] = "Display ALL Barista & Details"
        choices[3] = "Add New Employee"
        choices[4] = "Edit Employee"
        choices[5] = "Delete Employee"
        choices[6] = "Import from CSV file"
        choices[7] = "Export Data to a CSV file 'payroll.csv' "
        choices[8] = "Back to previous menu"
        choices[9] = "Exit"

        input_choice = select(choices,"Select from the functionalities below:") #FUNCTIONS CORRESPONDIDNG TO CHOICES
        if input_choice == 0 :
            DisplayEmployee(1)
        elif input_choice == 1:
            DisplayEmployee_byRole(1)
        elif input_choice == 2:
            DisplayEmployee_byRole(2)
        elif input_choice == 3:
            Ins_Employee()
        elif input_choice == 4:
            DisplayEmployee(0)
            Edi_Employee()
        elif input_choice == 5:
            DisplayEmployee(0)
            Del_Employee()
        elif input_choice == 6:
            import_export.Imp_data_from_csv()
        elif input_choice == 7:
            import_export.export_payroll()
        elif input_choice == 8:
            display_menu()
        elif input_choice == 9:
            sys.exit(0)










