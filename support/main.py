import time
from support import TimedRobot
from support.plant import Plant
from support.threadUtils import start_background_task
from support.visualization import Visualization

# Main simulated components
plant = None
vis = None
robot = None

# Simulation State
cur_hood_angle_deg = 0.0
cur_flywheel_spd_rpm = 0.0
time_until_goal_active_sec = 5.0
cur_goal_height_in = 0

time_remaining_sec = 60.0

hood_motor_cmd_v = 0.0
flywheel_motor_cmd_v = 0.0
should_launch = False

sim_running=True


def main(robot_in:TimedRobot):
    global time_remaining_sec
    global sim_running
    global plant
    global vis
    global robot

    # Do all init
    plant = Plant()
    vis = Visualization()
    robot = robot_in
    robot.robotInit()

    # Start Plant thread
    start_background_task(_plantUpdate, 0.02)

    # Start Robot Controls thread
    start_background_task(_robotUpdate, 0.02)

    vis.start()

    # Wait for simulation to finish
    while(time_remaining_sec > 0.0):
        time.sleep(0.1)

    # Mark the simulation as running
    sim_running = False

    # wait for user to close window
    while(vis.is_window_open()):
        time.sleep(0.1)



def _plantUpdate():
    global plant
    global vis
    global cur_hood_angle_deg
    global cur_flywheel_spd_rpm
    global time_until_goal_active_sec
    global cur_goal_height_in
    global time_remaining_sec
    global hood_motor_cmd_v
    global flywheel_motor_cmd_v
    global should_launch
    global sim_running

    if(sim_running):
        time_remaining_sec = max(0.0, time_remaining_sec - 0.02)
        vis.set_time_remaining(time_remaining_sec)

def _robotUpdate():
    global robot
    global cur_hood_angle_deg
    global cur_flywheel_spd_rpm
    global time_until_goal_active_sec
    global cur_goal_height_in
    global time_remaining_sec
    global hood_motor_cmd_v
    global flywheel_motor_cmd_v
    global should_launch
    global sim_running

    if(sim_running):
        hood_motor_cmd_v, flywheel_motor_cmd_v, should_launch = robot.robotPeriodic(cur_hood_angle_deg, cur_flywheel_spd_rpm, time_until_goal_active_sec, cur_goal_height_in)
