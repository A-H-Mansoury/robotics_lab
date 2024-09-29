import numpy as np
from Spad import Spad
from ForwardKinematic import forward_kinematic

def inverse_kinematic(X_, gamma, ROBOT_CONFIG):
    assert X_.shape == (3,1)
    assert -np.pi/2 <= gamma <= np.pi/2
    x,y,z = X_.ravel().copy()

    d1, a1, a2, a3, a4 = ROBOT_CONFIG.copy()

    t1 = np.arctan2(y,x+a1)

    t234 = np.arctan2(
        np.cos(t1)*np.sin(gamma), np.cos(gamma)
        )
    A = np.sqrt(y**2+(x+a1)**2)-a4*np.cos(t234)
    #y/np.sin(t1)-a4*np.cos(t234)
    B = z-d1-a4*np.sin(t234)
    # print((A**2+B**2-(a2**2+a3**2))/(2*a2*a3))
    t3 = +np.arccos(
            min((A**2+B**2-(a2**2+a3**2))/(2*a2*a3), 1)
        )
    C = a2+a3*np.cos(t3)
    D = a3*np.sin(t3)
    t2 = np.arctan2(
        -D*A+C*B,
        C*A+D*B
    )
    t4 = t234-t2-t3
    q = np.array([t1, t2, t3, t4]).reshape((4,1))
    return q


if __name__ == '__main__':
    sp = Spad()
    robot_config = sp.ROBOT_CONFIG

    #rad
    #home position
    # pos = [[337.],
    # [  0.],
    # [175.]]
    pos = [[200],
    [200],
    [ 150]]
    gamma = -30
    gamma = np.deg2rad(gamma)

    pos = np.array(pos)#.reshape((3,1))

    q = inverse_kinematic(pos, gamma, robot_config)
    print(np.rad2deg(q))

    if sp.check_position_limit_angle(q):
        sp.set_position_angle(q)
        sp.print_position_angles_deg()