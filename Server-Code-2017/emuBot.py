from pyax12.connection import Connection
import time
import threading

#Sometimes if USB2AX is bumped, name will change from /dev/ttyACM0 to /dev/ttyACM1.
for bump in range(3): #Check if USB2AX was bumped
        try:
                sc = Connection(port="/dev/ttyACM" + str(bump), baudrate=1000000)
        except:
                if bump == 2: #Assuming you didn't somehow bump it 3 times in a row in quick succession.
                        print("USB2AX does not seem to be connected!")
                pass

sc.flush()

# Set up a dynamixel so that it behaves like joint
def jointMode(ID):
        sc.set_cw_angle_limit(ID,0,False)
        sc.set_ccw_angle_limit(ID,1023,False)

# Set up a dynamixel so that it behaves like wheel
def wheelMode(ID):
        sc.set_ccw_angle_limit(ID,0,False)
        sc.set_cw_angle_limit(ID,0,False)

# Print useful information about an individual dynamixel servo
def readDxl(ID):
        sc.flush()
        sc.pretty_print_control_table(ID)

# Move a dynamixel that has been set up as a joint
def moveJoint(ID, position, speed):
        #print(ID,position,speed)
        sc.goto(int(ID), int(position), int(speed), False)

# Move a dynamixel that has been set up as a wheel
# Negative speed moves CW, positive speed moves CCW
def moveWheel(ID, speed):
        # Convert negative values of speed to between 1024 and 2047
        if speed < 0:
                # Limit allowed reverse speed to prevent errors
                if speed < -1024:
                        speed = 2047
                else:
                        speed = 1023 + -speed
                
        else:
                if speed > 1023:
                        # Limit allowed forward speed to prevent errors
                        speed = 1023
                 
        sc.flush()
        sc.goto(ID, 0, int(speed), degrees=False)


'''moveWheel(1,100)
moveWheel(2,100)
moveWheel(3,100)
moveWheel(4,100)
moveWheel(5,100)
moveWheel(6,100)
moveWheel(7,100)'''



