
from Spad import Spad
from time import sleep

if __name__ == '__main__':
    sp = Spad()
    sp.torque_modify('0000')
    
    for i in range(5):
        sp.print_position()
        sp.print_position_angles_rad()
        sp.print_position_angles_deg()
        sleep(1)
    
    sp.torque_modify('1111')
