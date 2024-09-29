from dynamixel_sdk import * # Uses Dynamixel SDK library
import numpy as np
class Spad:
    
    #attributes
    MY_DXL = 'MX_SERIES'

    # Control table address
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_PRESENT_POSITION       = 132
    ADDR_PROFILE_VELOCITY       = 112
    ADDR_MAXIMUM_POSITION_LIMIT = 48
    ADDR_MINIMUM_POSITION_LIMIT = 52
    
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
    DEVICENAME                  = 'COM7'

    # Set baudrate
    BAUDRATE                    = 1000000

    Motor_IDs = [1,2,3,4] 
    
    MAX_VELOCITY = 15

    # d1, a1, a2, a3, a4 = sp.ROBOT_CONFIG
    ROBOT_CONFIG = [    
    175, #d1
    50, #a1
    119, #a2 
    118, #a3
    150, #a4
    ]

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



    # def __del__(self):
    #     # Close port
    #     self.portHandler.closePort()
    

    def torque_modify(self, config):
        """
        purpose: enables or disables torque
        input parameters: config
        sample input: "0001" 
        """
        tmp = list(map(int,config))        
        for ID in self.Motor_IDs:
            # Enable Dynamixel Torque
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_TORQUE_ENABLE, tmp[ID-1])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print(f"Torques successfully modified to {config}!")

    def check_position_limit_angle(self, goal_position):
        """
        By default is not used. Add it when neeeded
        purpose: check limits of goal position here in software before sending them to motors
        input parameters: array of 4  bits
        sample input: [1200, 2000, 3000, 4000] 
        output: is given goals within limits or not
        """
        goal_position = self.angle2bit(goal_position)
        if not(1080 <= goal_position[0] <= 3080):
            print("Theta_0 is out of range!")        
        if not(1080 <= goal_position[1] <= 2500):
            print("Theta_1 is out of range!")
        if not(1080 <= goal_position[2] <= 2500):
            print("Theta_2 is out of range!")
        if not(1080 <= goal_position[3] <= 2500):
            print("Theta_3 is out of range!")
        return (1080 <= goal_position[0] <= 3080) and (1080 <= goal_position[1] <= 2500) and (1080 <= goal_position[2] <= 2500) and (1080 <= goal_position[3] <= 2500)
    
    def check_position_limit(self, goal_position):
        """
        By default is not used. Add it when neeeded
        purpose: check limits of goal position here in software before sending them to motors
        input parameters: array of 4  bits
        sample input: [1200, 2000, 3000, 4000] 
        output: is given goals within limits or not
        """
        if not(1080 <= goal_position[0] <= 3080):
            print("Theta_0 is out of range!")        
        if not(1080 <= goal_position[1] <= 2500):
            print("Theta_1 is out of range!")
        if not(1080 <= goal_position[2] <= 2500):
            print("Theta_2 is out of range!")
        if not(1080 <= goal_position[3] <= 2500):
            print("Theta_3 is out of range!")
        return (1080 <= goal_position[0] <= 3080) and (1080 <= goal_position[1] <= 2500) and (1080 <= goal_position[2] <= 2500) and (1080 <= goal_position[3] <= 2500)
    
    def set_position(self, goal_position_):
        """
        purpose: set robot to desired position
        input parameters: array of 4  bits
        sample input: [1200, 2000, 3000, 4000] 
        """
        goal_position = goal_position_.copy()
        if True:#self.check_position_limit(goal_position):
            for ID in self.Motor_IDs:
                # Write goal position
                dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_GOAL_POSITION, goal_position[ID-1])
                if dxl_comm_result != COMM_SUCCESS:
                    print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
                elif dxl_error != 0:
                    print("%s" % self.packetHandler.getRxPacketError(dxl_error))
                else:
                    print(f"Motor_{ID} was successfully set to {goal_position[ID-1]}")
    
    def set_position_angle(self, angles_):
        """
        purpose: set robot to desired position
        input parameters: array of 4 radian angles
        sample input: [0, 2.5, 1.15, 3.14] 
        """
        angles = angles_.copy()
        assert 0 <= abs(angles).max() <= np.pi
        bts = self.angle2bit(angles)
        self.set_position(bts)

    def get_position_angle(self):
        """
        purpose: get position in radians
        sample output: [0, 2.5, 1.15, 3.14] 
 
        """
        current_position = self.get_position()
        return self.bit2angle(current_position)

    def get_position(self):
        """
        purpose: get position in bits
        sample output: [1200, 2000, 3000, 4000] 
        """
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
        res = list(map(int, tmp))
        print(f'Current angles are:\t{res}') 

    def print_position_angles_rad(self):
        tmp = self.get_position_angle()
        print(f'Current angles are in radians:\t{tmp}') 
    
    def print_position_angles_deg(self):
        tmp = self.get_position_angle()
        tmp = np.rad2deg(tmp)
        print(f'Current angles are in degrees:\t{tmp}') 
    
    
   
    #to be modified and make more precise
    def angle2bit(self, angles):
        """
        purpose: convert radian angles to bits
        sample input: [0, 2.5, 1.15, 3.14] 
        sample output: [1200, 2000, 3000, 4000] 
        """
        res = angles.copy()
        res[0] = angles[0]/np.pi*(3080-1080)+2047
        res[1] = angles[1]/(np.pi/2)*(3073-2047)+2047
        res[2] = angles[2]/(np.pi/2)*(1050-2050)+2050
        res[3] = angles[3]/(np.pi/2)*(3050-2050)+2050
        return list(map(int,res))

    def bit2angle(self, bits):
        
        """
        purpose: convert bits to radian angles
        sample input: [1200, 2000, 3000, 4000]
        sample output: [0, 2.5, 1.15, 3.14]  
        """
        res = bits.copy()
        res[0] = (bits[0]-2047)*np.pi/(3080-1080)
        res[1] = (bits[1]-2047)*(np.pi/2)/(3073-2047)
        res[2] = (bits[2]-2050)*(np.pi/2)/(1050-2050)
        res[3] = (bits[3]-2050)*(np.pi/2)/(3050-2050)
        return res



    def set_Limit(self, ID, MAX_VELOCITY, MAXIMUM_POSITION_LIMIT, MINIMUM_POSITION_LIMIT):
        """
        purpose: set each motor position and velocity
        sample usage:  sp.set_Limit(ID=1, MAX_VELOCITY=15, MAXIMUM_POSITION_LIMIT=2500, MINIMUM_POSITION_LIMIT=1500)
        """
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_PROFILE_VELOCITY, MAX_VELOCITY)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print(f"Motor_{ID}: Velocity Limit was successfully setted to {MAX_VELOCITY}!")

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_MAXIMUM_POSITION_LIMIT, MAXIMUM_POSITION_LIMIT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print(f"Motor_{ID}: Maximum Position Limit was successfully setted to {MAXIMUM_POSITION_LIMIT}!")

        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_MINIMUM_POSITION_LIMIT, MINIMUM_POSITION_LIMIT)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        else:
            print(f"Motor_{ID}: Minimum Position Limit was successfully setted to {MINIMUM_POSITION_LIMIT}!")


# np.deg2rad(q).reshape((4,1))
