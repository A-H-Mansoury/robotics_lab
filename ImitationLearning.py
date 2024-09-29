from time import *
from Spad import *
import datetime

if __name__ == '__main__1':

    steps = 6
    now = time.time()
    print(now)
    goal_positions = []
    for i in range(1, steps + 1):
        sleep(5)
        goal_position = [i,i,i,i] 
        goal_positions.append(goal_position)
        print(f"sample#{i}  :  {goal_position}")

    sleep(2)
    print("running now")
    sleep(2)

    for pos in range(steps):

        print(goal_positions[pos])
        sleep(5)


if __name__ == '__main__':

    steps = 200
    sp = Spad()
    sp.torque_modify('0000')

    print("sampling started")

    goal_positions = []
    times = [] 
    T=0.2   
    for i in range(steps):
        #sleep(T)
        #now = time.time()
        goal_position = sp.get_position(return_angle=False)
        goal_positions.append(goal_position)
        #times.append(now)
        print(f"sample# {i}  :  {goal_position}")

    sleep(2)
    print("sampling finished - now sampels will send to robot")
    sp.torque_modify('1111')
    sp.set_position(goal_positions[0])
    print(goal_positions[0])
    sleep(6)
    print("running started")

    for pos in range(steps):
        sp.set_position(goal_positions[pos])
        print(f"position#{pos} :  goal_positions[pos]  sent to robot")
        sleep(T)

