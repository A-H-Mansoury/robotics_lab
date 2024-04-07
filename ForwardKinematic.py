import numpy as np

def generate_H(theta, d, a, alpha):
    s = np.sin
    c = np.cos
    tmp = [
        [c(theta), -s(theta)*c(alpha), -s(theta)*s(alpha), a*c(theta)],
        [s(theta), c(theta)*c(alpha), -c(theta)*s(alpha), a*s(theta)],
        [0, s(alpha), c(alpha), d],
        [0, 0, 0, 1]
    ]
    return np.array(tmp)

def H_all(t1,t2,t3,t4):
    d1 = 180
    a1 = 50
    a2 = 120
    a3 = 120
    a4 = 150
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

H = H_all(np.pi/4, 0, 0, 0)

P=np.array([[0],[0],[0],[1]])
P_EE = np.matmul(
    H, 
    P
)
print(P_EE)