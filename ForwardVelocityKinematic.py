import numpy as np
from Spad import Spad
from time import sleep

def substitute_jacobian(q_, ROBOT_CONFIG):
    q = q_.copy()

    assert -np.pi<= abs(q).max() <= np.pi
    assert q.shape == (4,1)
    q1,q2,q3,q4 = q.ravel()
    d1, a1, a2, a3, a4 = ROBOT_CONFIG.copy()
    
    s=np.sin
    c=np.cos
    J = [
        [-s(q1)*(a2*c(q2)+a3*c(q2+q3)+a4*c(q2+q3+q4)), c(q1)*(-a2*s(q2)-a3*s(q2+q3)-a4*s(q2+q3+q4)),c(q1)*(-a3*s(q2+q3)-a4*s(q2+q3+q4)),c(q1)*(-a4*s(q2+q3+q4)) ],
        [c(q1)*(a2*c(q2)+a3*c(q2+q3)+a4*c(q2+q3+q4)), s(q1)*(-a2*s(q2)-a3*s(q2+q3)-a4*s(q2+q3+q4)),s(q1)*(-a3*s(q2+q3)-a4*s(q2+q3+q4)),s(q1)*(-a4*s(q2+q3+q4)) ], 
        [0,a2*c(q2) + a3*c(q2+q3) + a4*c(q2+q3+q4), a3*c(q2+q3) + a4*c(q2+q3+q4), a4*c(q2+q3+q4) ] 
        ]
    
    J = np.array(J)
    assert J.shape == (3,4)

    return J



def forward_velocity_kinematic(q_, dq_, ROBOT_CONFIG):

    q = q_.copy()
    dq = dq_.copy()

    assert 0 <= abs(q).max() <= np.pi
    assert q.shape == (4,1)

    assert 0 <= abs(dq).max() <= np.pi/4
    assert dq.shape == (4,1)

    J = substitute_jacobian(q, ROBOT_CONFIG=ROBOT_CONFIG)
    dX = np.matmul(J, dq)

    assert dX.shape == (3, 1)

    return dX


if __name__ == '__main__':
    #use when connected to robot
    sp = Spad()
    robot_config = sp.ROBOT_CONFIG


    q =  [15,10,0,0]
    q = np.deg2rad(q).reshape((4,1))
    sp.set_position_angle(q)

    J = substitute_jacobian(q, ROBOT_CONFIG=robot_config)
    print(J)
    
    sleep(5)
    
    dq = [0, 10, 0, 0]
    dq = np.deg2rad(dq).reshape((4,1))
    
    sp.set_position_angle(q+dq)
    
    dX = forward_velocity_kinematic(q, dq, ROBOT_CONFIG=robot_config)   
    
    print(dX)