import numpy as np
from Spad import Spad

def generate_H(theta, d, a, alpha):
    s = np.sin
    c = np.cos
    tmp = [
        [c(theta), -s(theta)*c(alpha), s(theta)*s(alpha), a*c(theta)],
        [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
        [0, s(alpha), c(alpha), d],
        [0, 0, 0, 1]
    ]
    return np.array(tmp)

def H_all(t1,t2,t3,t4, ROBOT_CONFIG):
    d1, a1, a2, a3, a4 = ROBOT_CONFIG.copy()
    dh = [
        [0, 0, -a1, 0],
        [t1, d1, 0, np.pi/2],
        [t2, 0, a2, 0],
        [t3, 0, a3, 0],
        [t4, 0, a4, 0]
    ]
    theta, d, a, alpha = dh[0]
    H = generate_H(theta, d, a, alpha)
    for theta, d, a, alpha in dh[1:]:
        tmp = generate_H(theta, d, a, alpha)
        H = np.matmul(H, tmp)
    return H

def forward_kinematic(q, ROBOT_CONFIG):
    """
    purpose: calculate forward kinematics
    input: a 4*1 vector of radian angles
    output: a 3*1 vector of x y z position in millimeters 
    sample input: np.array([[0], [2.5], [1.15], [3.14]])
    sample output: array([[127], [10], [120]])
    """
    #make sure all angles are in radians
    q = q.copy()
    
    assert 0 <= abs(q).max() <= np.pi
    assert q.shape == (4,1)

    q = q.ravel()

    H = H_all(*q,  ROBOT_CONFIG)

    P=np.array([[0],[0],[0],[1]])
    P_EE = np.matmul(
        H, 
        P
    )
    P_EE = P_EE[:-1]
    assert P_EE.shape == (3, 1)
    return P_EE

if __name__ == '__main__':
    #use when connected to robot
    sp = Spad()
    robot_config = sp.ROBOT_CONFIG

    q = [0, 0, 0, 0]
    q = np.deg2rad(q).reshape((4,1))
        
    sp.set_position_angle(q)

    _ = forward_kinematic(q, ROBOT_CONFIG=robot_config)
    
    print("The result of forward kinematics is\t %s"% str(_))
