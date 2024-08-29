

class Plant():
    def __init__(self):
        pass

    def plantUpdate(self, hood_motor_cmd_v, flywheel_motor_cmd_v, should_launch):

        cur_hood_angle_deg = 0
        cur_flywheel_spd_rpm = 0
        time_until_goal_active_sec = 0
        cur_goal_height_in = 0


        return (cur_hood_angle_deg, cur_flywheel_spd_rpm, time_until_goal_active_sec, cur_goal_height_in)
