from InverseVelocityKinematics import inverse_velocity_kinematic
from ForwardKinematic import forward_kinematic
from Spad import Spad
import numpy as np
from time import sleep
#set limits
# if __name__ == '__main__':
#     sp = Spad()
#     sp.torque_modify("0000")
#     sp.set_Limit(
#        1, MAX_VELOCITY=15, MAXIMUM_POSITION_LIMIT=3080, MINIMUM_POSITION_LIMIT=1080
#     )
#     sp.set_Limit(
#        2, MAX_VELOCITY=15, MAXIMUM_POSITION_LIMIT=2500, MINIMUM_POSITION_LIMIT=1500
#     )
#     sp.set_Limit(
#        3, MAX_VELOCITY=15, MAXIMUM_POSITION_LIMIT=2500, MINIMUM_POSITION_LIMIT=1500
#     )
#     sp.set_Limit(
#        4, MAX_VELOCITY=15, MAXIMUM_POSITION_LIMIT=2500, MINIMUM_POSITION_LIMIT=1080
#     )
        
#     sp.torque_modify("1111")


# if __name__ == '__main__':
#     sp = Spad()
#     sp.torque_modify("1111")

#go to home position

def goto(q_):
    q = q_.copy()
    q = np.deg2rad(q).reshape((4,1))
    assert 0 <= abs(q).max() <= np.pi
    assert q.shape == (4,1)
    sp = Spad()
    robot_config = sp.ROBOT_CONFIG
    print(
        forward_kinematic(q, ROBOT_CONFIG=robot_config)
        )
    sp.set_position_angle(q)

def angle2angle(q0, qd):
    sp = Spad()
    #use when connected to robot
    robot_config = sp.ROBOT_CONFIG


    q0 = np.deg2rad(q0).reshape((4,1))
    qd = np.deg2rad(qd).reshape((4,1))

    X0 = forward_kinematic(q0, ROBOT_CONFIG=robot_config)
    sp.set_position_angle(q0)

    sleep(5)
    print("program started")
    
    Xd = forward_kinematic(qd, ROBOT_CONFIG=robot_config)

    epsilon = 1
    alpha = 0.9

    Xc = X0
    qc = q0
    DX = Xd-Xc

    while np.linalg.norm(DX, 2) > epsilon:
        dX = alpha*(DX)/np.linalg.norm(DX, 2)
        dq = inverse_velocity_kinematic(dX.copy(), qc.copy(), ROBOT_CONFIG=robot_config)
        qc = qc+dq
        
        ######  send to the robot  #####################
        bts = sp.angle2bit(qc.copy().ravel()) 
        sp.set_position(bts)
        ################################################
        Xc = forward_kinematic(qc.copy(), ROBOT_CONFIG=robot_config)
        DX = Xd-Xc      
    print("error")
    print(Xd-Xc)


if __name__ == '__main__':
#     q = [-30, 30, 10, -30]
#     goto(q)
    q0 = [-20,20,10,10]
    qd = [45, -10, 30, 0]
    angle2angle(q0, qd)