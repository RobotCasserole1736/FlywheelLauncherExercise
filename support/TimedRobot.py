

class TimedRobot():
    def robotInit(self):
        pass
    def robotPeriodic(self, cur_hood_angle_deg, cur_flywheel_spd_rpm, time_until_goal_active_sec, cur_goal_height_cm):
        return (0,0,False) # Hood Motor Voltage, Flywheel Voltage, Should Launch
