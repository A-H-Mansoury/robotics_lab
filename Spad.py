from dynamixel_sdk import *  # Importing necessary modules from Dynamixel SDK library

class Spad:
    
    # Attributes
    MY_DXL = 'MX_SERIES'  # A string attribute specifying the type of Dynamixel motors used

    # Control table addresses for various parameters
    ADDR_TORQUE_ENABLE          = 64
    ADDR_GOAL_POSITION          = 116
    ADDR_PRESENT_POSITION       = 132
    ADDR_PROFILE_VELOCITY       = 112
    ADDR_MAXIMUM_POSITION_LIMIT = 52
    ADDR_MINIMUM_POSITION_LIMIT = 48
    
    MINIMUM_POSITION_LIMIT = 1500  # Default minimum position limit
    MAXIMUM_POSITION_LIMIT = 2500  # Default maximum position limit
    
    # Defines
    TORQUE_ENABLE               = 1     # Value for enabling the torque
    TORQUE_DISABLE              = 0     # Value for disabling the torque
    DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold

    # DYNAMIXEL Protocol Version (1.0 / 2.0)
    PROTOCOL_VERSION = 2.0

    # Use the actual port assigned to the U2D2.
    DEVICENAME = 'COM6'  # Specify the device name (serial port)

    # Set baudrate
    BAUDRATE = 100000  # Baudrate for communication with Dynamixel motors

    Motor_IDs = [1,2,3,4]  # List of motor IDs connected

    MAX_VELOCITY = 15  # Maximum velocity allowed

    # Methods

    def __init__(self):
        # Initialize the port handler
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

        # Modify torque settings before setting position limits
        self.torque_modify('0000')
        self.set_Limit()
        # Re-enable torque after setting position limits
        self.torque_modify('1111')

    def __del__(self):
        # Destructor to close the port when the object is destroyed
        self.portHandler.closePort()

    # Method to modify torque settings for the motors
    def torque_modify(self, En, config='1111'):
        tmp = list(map(int,config))  # Convert 'config' string to a list of integers
        for ID in self.Motor_IDs:
            # Enable or disable Dynamixel Torque based on 'En' parameter
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_TORQUE_ENABLE, tmp[ID-1])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")

    # Method to set desired positions for the motors
    def set_position(self, goal_position = []):
        for ID in self.Motor_IDs:
            # Write goal position to each motor
            dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, ID, self.ADDR_GOAL_POSITION, goal_position[ID-1])
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))

    # Method to get current positions of the motors
    def get_position(self):
        current_position = []
        for ID in self.Motor_IDs:
            # Read present position of each motor
            dxl_present_position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, ID, self.ADDR_PRESENT_POSITION)
            current_position.append(dxl_present_position)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
        return current_position

    # Method to print current positions of the motors
    def print_position(self):
        print(f'Current positions are:\t{self.get_position()}') 

    # Method to set position limits and maximum velocity for the motors
    def set_Limit(self):
        for ID in self.Motor_IDs:
            # Set maximum velocity
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_PROFILE_VELOCITY, self.MAX_VELOCITY)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")

            # Set maximum position limit
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_MAXIMUM_POSITION_LIMIT, self.MAXIMUM_POSITION_LIMIT)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")

            # Set minimum position limit
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, ID, self.ADDR_MINIMUM_POSITION_LIMIT, self.MINIMUM_POSITION_LIMIT)
            if dxl_comm_result != COMM_SUCCESS:
                print("%s" % self.packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("%s" % self.packetHandler.getRxPacketError(dxl_error))
            else:
                print("Dynamixel has been successfully connected")
                

if __name__ == '__main__':
    # If this script is executed as the main program:

    # Create an instance of the Spad class
    sp = Spad()

    # Print the current positions of the motors
    sp.print_position()

    # Set the desired positions for the motors to [1600, 1600, 1600, 1600]
    sp.set_position([1600, 1600, 1600, 1600])
