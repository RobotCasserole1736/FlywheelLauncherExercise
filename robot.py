####################################################################
## Main robot function - user code should be put here
####################################################################

from support.TimedRobot import TimedRobot
from support.main import main



class MyRobot(TimedRobot):

    def robotInit(self):
        pass
        # TODO - Add your init code here

    def robotPeriodic(self, cur_hood_angle_deg, cur_flywheel_spd_rpm, time_until_goal_active_sec, cur_goal_height_cm):
        
        # TODO - this is a very simple strategy. It rarely works.
        # Pick a new strategy for calculating each variable that scores more points.
        hood_motor_cmd_v =-1.0
        flywheel_motor_cmd_v = 5.0
        should_launch = (time_until_goal_active_sec == 0)

        # Do not change code below this line
        return (hood_motor_cmd_v,flywheel_motor_cmd_v,should_launch) 



# Do not modify
if __name__ == "__main__":
    main(MyRobot())

