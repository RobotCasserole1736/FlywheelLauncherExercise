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
cur_goal_height_cm = 0

time_remaining_sec = 60.0

hood_motor_cmd_v = 0.0
flywheel_motor_cmd_v = 0.0
should_launch = False


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




def _plantUpdate():
    global plant
    global vis
    global cur_hood_angle_deg
    global cur_flywheel_spd_rpm
    global time_until_goal_active_sec
    global cur_goal_height_cm
    global time_remaining_sec
    global hood_motor_cmd_v
    global flywheel_motor_cmd_v
    global should_launch

    if(time_remaining_sec > 0.0):
        time_remaining_sec = max(0.0, time_remaining_sec - 0.02)
        vis.set_time_remaining(time_remaining_sec)
        (cur_hood_angle_deg, cur_flywheel_spd_rpm, time_until_goal_active_sec, cur_goal_height_cm, ball_coords, ball_active, cur_score) = plant.plantUpdate(hood_motor_cmd_v, flywheel_motor_cmd_v,should_launch)
        vis.set_ball_position(ball_coords[0], ball_coords[1], ball_active)
        vis.set_hood_extension(cur_hood_angle_deg)
        vis.set_shooter_speed(cur_flywheel_spd_rpm)
        vis.set_goal_lit_up(time_until_goal_active_sec == 0.0)
        vis.set_goal_position(cur_goal_height_cm)
        vis.set_score(cur_score)
        vis.set_telemetry(cur_flywheel_spd_rpm, cur_hood_angle_deg,time_until_goal_active_sec,cur_goal_height_cm)

def _robotUpdate():
    global robot
    global cur_hood_angle_deg
    global cur_flywheel_spd_rpm
    global time_until_goal_active_sec
    global cur_goal_height_cm
    global time_remaining_sec
    global hood_motor_cmd_v
    global flywheel_motor_cmd_v
    global should_launch

    if(time_remaining_sec > 0.0):
        hood_motor_cmd_v, flywheel_motor_cmd_v, should_launch = robot.robotPeriodic(cur_hood_angle_deg, cur_flywheel_spd_rpm, time_until_goal_active_sec, cur_goal_height_cm)
