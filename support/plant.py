import math
import random

from support.filter import ExpFilter
BALL_LAUNCH_X = 150.0
BALL_LAUNCH_Y = 100.0
SCORE_LINE_X = 550.0
SCORE_GOAL_MARGIN_Y = 60.0

def saturate(val, min, max):
    if(val < min):
        return min
    elif(val > max):
        return max
    else:
        return val
    
def sign(val):
    if(val > 0):
        return 1.0
    elif(val < 0):
        return -1.0
    else:
        return 0.0

class Plant():
    def __init__(self):
        self.cur_hood_angle_deg = 0
        self.cur_flywheel_spd_rpm = 0
        self.time_until_goal_active_sec = 0
        self.cur_goal_height_cm = 0

        self.ACTIVE_DWELL_TIME_SEC = 2.25
        self.ball_active = False
        self.ball_coords = [BALL_LAUNCH_X,BALL_LAUNCH_Y]
        self.ball_coords_prev = [BALL_LAUNCH_X,BALL_LAUNCH_Y]
        self.ball_vel = [0,0]

        self.flywheelExpFilter = ExpFilter(0.05) # constant controls accel
        self.hoodExpFilter = ExpFilter(0.1)
        self.goalHeightExpFilter = ExpFilter(0.15)

        self.goal_active_timer = self.ACTIVE_DWELL_TIME_SEC
        self.goal_height_tgt = 100

        self.cur_score = 0

    def plantUpdate(self, hood_motor_cmd_v, flywheel_motor_cmd_v, should_launch):

        ######################################################################################
        # Ball Plant
        if(should_launch and not self.ball_active):
            self.ball_active = True
            self.ball_coords = [BALL_LAUNCH_X,BALL_LAUNCH_Y]
            launchAngle = self.cur_hood_angle_deg * ( math.pi / 180)
            self.ball_vel[0] = math.cos(launchAngle) * self.cur_flywheel_spd_rpm  * 0.6
            self.ball_vel[1] = math.sin(launchAngle) * self.cur_flywheel_spd_rpm  * 0.6

        if(self.ball_active):

            # sorta kinda air resistance
            netVel = math.hypot(self.ball_vel[0], self.ball_vel[1])
            self.ball_vel[0] -= 0.02 * (netVel*netVel) * 0.0025 * sign(self.ball_vel[0])
            self.ball_vel[1] -= 0.02 * (netVel*netVel) * 0.0025 * sign(self.ball_vel[1])

            # acceleration due to gravity
            self.ball_vel[1] += -800.0 * 0.02

            # Bounce
            if(self.ball_coords[1] <= 0.0):
                self.ball_coords[1] = 0.0
                self.ball_vel[1] *= -0.50
                self.ball_vel[0] *= 0.80

            # Velocity update
            self.ball_coords[0] += self.ball_vel[0] * 0.02
            self.ball_coords[1] += self.ball_vel[1] * 0.02

            # Off the screen or too slow, no longer active
            netVel = math.hypot(self.ball_vel[0], self.ball_vel[1])
            offScreen = self.ball_coords[0] > 850.0 
            tooSlow = netVel < 10.0 and self.ball_coords[1] < 5
            if(offScreen or tooSlow):
                self.ball_active = False

        ######################################################################################
        # Goal Plant
        if(self.time_until_goal_active_sec <= 0.0):
            self.goal_active_timer -= 0.02
            if(self.goal_active_timer <= 0.0):
                # transition to new active position
                self.time_until_goal_active_sec = random.uniform(1.0, 3.0)
                self.goal_height_tgt = int(random.uniform(50,300))

        else:
            self.time_until_goal_active_sec -= 0.02
            self.goal_active_timer = self.ACTIVE_DWELL_TIME_SEC

        self.cur_goal_height_cm = self.goalHeightExpFilter.smooth(self.goal_height_tgt)
        self.time_until_goal_active_sec = saturate(self.time_until_goal_active_sec, 0.0, 100.0)

        ######################################################################################
        # Ball/Goal score Plant
        if(self.ball_active):
            if(self.ball_coords_prev[0] < SCORE_LINE_X and self.ball_coords[0] >= SCORE_LINE_X):
                # ball is active and just passed the score line
                if(abs(self.ball_coords[1] - self.cur_goal_height_cm) < SCORE_GOAL_MARGIN_Y):
                    # Score! 
                    self.cur_score += 1
                    #Immedeately cycle to next position
                    self.goal_active_timer = 0.0


        ######################################################################################
        # Hood Plant
        voltage = saturate(hood_motor_cmd_v, -12.0, 12.0)
        self.cur_hood_angle_deg += -1.0 * self.hoodExpFilter.smooth(voltage) * 0.02 * 3
        self.cur_hood_angle_deg = saturate(self.cur_hood_angle_deg, -60, 60)

        ######################################################################################
        # Flywheel Plant
        voltage = saturate(flywheel_motor_cmd_v, 0.0, 12.0)
        self.cur_flywheel_spd_rpm = self.flywheelExpFilter.smooth(voltage) * 5800 / 12.0

        self.ball_coords_prev[0] = self.ball_coords[0]
        self.ball_coords_prev[1] = self.ball_coords[1]

        return (self.cur_hood_angle_deg, self.cur_flywheel_spd_rpm, self.time_until_goal_active_sec, self.cur_goal_height_cm, self.ball_coords, self.ball_active, self.cur_score)
