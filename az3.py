from dynamixel_sdk import * # Uses Dynamixel SDK library
from time import sleep
class Spad:
    
    #attributes
    MY_DXL = 'MX_SERIES'

    # Control table address
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_PRESENT_POSITION       = 132
    ADDR_PROFILE_VELOCITY       = 112
    ADDR_MAXIMUM_POSITION_LIMIT = 52
    ADDR_MINIMUM_POSITION_LIMIT = 48
    
    MINIMUM_POSITION_LIMIT  = 1500           
    MAXIMUM_POSITION_LIMIT  = 2500           
    
    # Defines
    TORQUE_ENABLE               = 1     # Value for enabling the torque
    TORQUE_DISABLE              = 0     # Value for disabling the torque
    DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold


    # DYNAMIXEL Protocol Version (1.0 / 2.0)
    PROTOCOL_VERSION            = 2.0

    # Use the actual port assigned to the U2D2.
    # ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
    DEVICENAME                  = 'COM6'

    # Set baudrate
    BAUDRATE                    = 1000000

    Motor_IDs = [1,2,3,4] 
    
    MAX_VELOCITY = 15

    #methods

    def __init__(self):
        portHandler = PortHandler(self.DEVICENAME)
        # Initialize PacketHandler instance
        self.packetHandler = PacketHandler(self.PROTOCOL_VERSION)

        # Open port
        if portHandler.openPort():
            print("Succeeded to open the port")
        else:
            print("Failed to open the port")
            print("Press any key to terminate...")


        # Set port baudrate
        if portHandler.setBaudRate(self.BAUDRATE):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            print("Press any key to terminate...")
        
        self.portHandler = portHandler

        self.torque_modify('0000')
        self.set_Limit()
        self.torque_modify('1111')


    def __del__(self):
        # Close port
        self.portHandler.closePort()
    


    def torque_modify(self, config):
        tmp = list(map(int,config))        
        for ID in self.Motor_IDs:
            # Enable Dynamixel Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_TORQUE_ENABLE, tmp[ID-1])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")


    def set_position(self, goal_position = []):
        for ID in self.Motor_IDs:
            # Write goal position
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_GOAL_POSITION, goal_position[ID-1])
            
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    def get_position(self):
        current_position = []
        for ID in self.Motor_IDs:
            # Read present position
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, ID, self.ADDR_PRESENT_POSITION)
            current_position.append(dxl_present_position)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

        return current_position

    def print_position(self):
        tmp = self.get_position()
        res = tmp
        res[0] = tmp[0]*180/(3080-1080)-180
        res[1] = tmp[1]*90/(3073-2047)-180
        res[2] = tmp[2]*90/(1050-2050)+180
        res[3] = tmp[3]*90/(3050-2050)-180

        #res = [round(i,4) for i in res]
        res = list(map(int, res))
        print(f'Current positions are:\t{res}') 


    def set_Limit(self):
        for ID in self.Motor_IDs:
            
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_PROFILE_VELOCITY, self.MAX_VELOCITY)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")

            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_MAXIMUM_POSITION_LIMIT, self.MAXIMUM_POSITION_LIMIT)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")

            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_MINIMUM_POSITION_LIMIT, self.MINIMUM_POSITION_LIMIT)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")






if __name__ == '__main__':
    sp = Spad()

    #    sp.torque_modify('0000')
    #    while(True):
        
    #     sp.print_position()
    #     sleep(1)

    #    sp.torque_modify('0000')

    sp.torque_modify('1111')


