from ForwardVelocityKinematic import substitute_jacobian
from Spad import Spad
import numpy as np

def right_pseudo_inverse(J_):
    J = J_.copy()
    assert J.shape == (3, 4)

    Jt = J.T
    JJ_t = np.matmul(J, Jt)
    JJ_t_inv = np.linalg.inv(JJ_t)
    rpi = np.matmul(Jt, JJ_t_inv)

    assert rpi.shape == (4, 3)

    return rpi

def inverse_velocity_kinematic(dX_, q_, ROBOT_CONFIG):
    """
    purpose: calculate inverse kinematics
    input q : a 4*1 vector of radian angles
    input dX : a 3*1 vector of x y z differential position in millimeters 
    input ROBOT_CONFIG: fetch from Spad class
    sample input q : np.array([[0], [2.5], [1.15], [3.14]])
    sample input dX : np.array([[10], [2], [5]])
    output dq: a 4*1 vector diffential angles in radian 
    sample dq: np.array([[0.5], [0.5], [0.15], [0.25]])
    """
    dX = dX_.copy()
    q = q_.copy()

    assert 0 <= abs(q).max() <= 100
    assert dX.shape == (3,1)

    assert 0 <= abs(q).max() <= np.pi
    assert q.shape == (4,1)

    J = substitute_jacobian(q, ROBOT_CONFIG=ROBOT_CONFIG)
    J_rpi = right_pseudo_inverse(J)
    dq = np.matmul(J_rpi, dX)
    
    assert dq.shape == (4,1)

    return dq

if __name__ == '__main__':
    #use when connected to robot
    sp = Spad()
    robot_config = sp.ROBOT_CONFIG

    #dX =#np.array([1,  ,  0]).reshape((3,1))
    dX = np.array([[-23.77053574],
    [-13.72392521],
    [  7.97714992]])

    q =  [30,30,30,30]
    
    q = np.deg2rad(q).reshape((4,1))


    dq = inverse_velocity_kimematic(dX, q, ROBOT_CONFIG=robot_config)
    # dq = np.rad2deg(dq)
    # dq = np.round(dq, 5)
    # print(
    #     dq
    # )

    # vis = Visualization()

    # X1 = forward_kinematic(q,ROBOT_CONFIG=robot_config)
    # X1 += dX
    # vis.plot_point(X1, "#d62728")
    
    # q += dq
    # X2 = forward_kinematic(q,ROBOT_CONFIG=robot_config)
    # vis.plot_point(X2, "#9467bd")
    
    # vis.show()