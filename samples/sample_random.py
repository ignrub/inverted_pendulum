# -*- coding: utf-8 -*-

try:
    import vrep
except:
    print '--------------------------------------------------------------'
    print '"vrep.py" could not be imported. This means very probably that'
    print 'either "vrep.py" or the remoteApi library could not be found.'
    print 'Make sure both are in the same folder as this file,'
    print 'or appropriately adjust the file "vrep.py"'
    print '--------------------------------------------------------------'

import time
import math
import sys
import random

random.seed()

clientID = -1

def start_simulator():
    global clientID

    print 'Program started'
    vrep.simxFinish(-1)
    clientID = vrep.simxStart('127.0.0.1', 19999, True, True, 5000, 5)

    if clientID != -1:
        print 'Connected to remote API server'
    else:
        print 'Failed connecting to remote API server'
        sys.exit('Program Ended')

def error_check(res):
    global clientID

    if res != vrep.simx_return_ok:
        print 'Failed to get sensor Handler'
        vrep.simxFinish(clientID)
        sys.exit('Program ended')

def main():
    global clientID

    res, objs = vrep.simxGetObjects(clientID, vrep.sim_handle_all, vrep.simx_opmode_oneshot_wait)
    error_check(res)
    res, JointDynamic = vrep.simxGetObjectHandle(clientID, "joint" , vrep.simx_opmode_oneshot_wait)
    error_check(res)
    res, Potentiometer = vrep.simxGetObjectHandle(clientID, "Potentiometer", vrep.simx_opmode_oneshot_wait)
    error_check(res)

    time.sleep(1.0)

    #set joint truqe
    vrep.simxSetJointForce(clientID, JointDynamic, 4.8, vrep.simx_opmode_oneshot)

    while True:
        #Get Potentiometer
        res, pos = vrep.simxGetJointPosition(clientID, Potentiometer, vrep.simx_opmode_oneshot)
        print "Potentiometer: %lf[deg]" % math.degrees(pos)
        
        #Decide about joint velocities:
        linearVelocity  = random.random() * random.choice((-20, 20))
        
        vrep.simxSetJointTargetVelocity(clientID, JointDynamic, linearVelocity, vrep.simx_opmode_oneshot)
        
        time.sleep(0.001)

if __name__ == '__main__':
    start_simulator()
    main()
