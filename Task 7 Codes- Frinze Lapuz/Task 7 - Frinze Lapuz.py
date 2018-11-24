# Name: Frinze Lapuz
#MAIN
# This file is responsible in testing specific portions of the project
# As to avoid certain prerequisites that slows down testing such as needing to authenticate everytime just to test
# THIS IS THE ONLY FILE that has lines of code in the main line so that when importing specific .py file
# Other functionalities won't interfere
# Eg. File1 and File2
# File1{
#     print("a")
#     import File2
#   }
#
# File2{
#      print("b")
#      import File1
# }
# If one of them runs, it creates an infinite loop outputting abababababa ...
#
# The point of dividing the project into different .py is to organize all the related functions

import Internal_Processing
Internal_Processing.display_menu()
##
#import import_export
#import_export.export_payroll()
