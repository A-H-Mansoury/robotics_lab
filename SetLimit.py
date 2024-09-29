
from Spad import Spad

if __name__ == '__main__':
    sp = Spad()
    sp.torque_modify('0000')
    sp.set_Limit(1, 15, 3080, 1080)
    sp.set_Limit(2, 15, 3080, 1080)
    sp.set_Limit(3, 15, 3080, 1080)
    sp.set_Limit(4, 15, 3080, 1080)
    sp.torque_modify('1111')