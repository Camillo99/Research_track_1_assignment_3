#! /usr/bin/env python

import rospy
from a3_code.srv import Keyboard_type	#used in case 2,3
from a3_code.srv import Coordinate_xy	#used in case 1

#print the option menu on terminal and wait for a numerical answer by the user
def opt_menu():
    print("1) autonomously reach a x,y coordinate provided by the user")
    print("2) drive the robot using the keyboard")
    print("3) drive the robot using the keyboard with collisions avoidance")
    print("0) quit the program")
    print()        
    return input("select an action: ")

#get from the user the specific (x,y) coordinate and send it to the handler service
#for this option
#if the target is reached (or not) print a response from the service   
def option1():
    print("case 1")
    x = float(input("insert x: "))
    y = float(input("insert y: "))
    rospy.wait_for_service('coordinate_xy')
    coordinate_xy = rospy.ServiceProxy('coordinate_xy', Coordinate_xy)
    rt = coordinate_xy(x , y)
    if rt.return_ == 1:
        print("target reached successfully!")
    else:
      	print("target not reached")

#call the keyboard service to handle the case           	
def option2():
    print("case 2")
    rospy.wait_for_service('keyboard_type')
    keyboard_type = rospy.ServiceProxy('keyboard_type', Keyboard_type)
    keyboard_type(1)

#call the keyboard service to handle the case
def option3():
    print("case 3")
    rospy.wait_for_service('keyboard_type')
    keyboard_type = rospy.ServiceProxy('keyboard_type', Keyboard_type)
    keyboard_type(2)


 
if __name__=="__main__":
    #initialize the ros node
    rospy.init_node('user_controller')

    flag = 1
    while(flag):
        #print all the possible action which the user can performs
        #store the answer of the user in variable 'ans'
        ans = opt_menu()
        
        #check the validity of the answer
        if ans.isnumeric():
            ans = int(ans)
            if (ans == 1):
                #case 1
                option1()
            elif (ans == 2):
                #case 2
                option2()  
            elif (ans == 3):
                #case 3    
                option3()
            elif (ans == 0):
                #quit case
            	flag = 0
            	print("press ctrl-C to quit")
            	print()
            else:
                #incorrect input
                print("incorrect input!!")
        else:
            #non numerical input
            print("input value is not a number!!")
           
