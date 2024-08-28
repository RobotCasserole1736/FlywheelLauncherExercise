import tkinter as tk
import math
import threading
import time

class Visualization:
    def __init__(self):
        # Initialize the main window and canvas
        self.root = tk.Tk()
        self.root.title("FRC Robot Visualization")
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg='white')
        self.canvas.pack()

        # Robot parameters
        self.robot_length = 50
        self.robot_height = 30
        self.robot_x = 100
        self.robot_y = 350 - self.robot_height

        # Shooter parameters
        self.shooter_radius = 10
        self.shooter_center = (self.robot_x + self.robot_length, self.robot_y)
        self.shooter_wheel_speed = 0  # radians per second
        self.shooter_mark_angle = 0  # Initial angle for shooter wheel marking
        self.hood_angle = 0  # Hood extension in degrees from vertical

        # Ball parameters
        self.ball_diameter = 10
        self.ball_position = (self.robot_x, self.robot_y)
        self.ball_visible = False

        # Goal parameters
        self.goal_x = self.robot_x + 5 * self.robot_length
        self.goal_center_y = 200
        self.goal_width = 20
        self.goal_height = 60
        self.goal_lit_up = False

        # Draw initial setup
        self._draw_robot()
        self._draw_goal()

        # Start the animation thread
        self.running = True
        self.animation_thread = threading.Thread(target=self._animate)
        self.animation_thread.start()

    def _draw_robot(self):
        # Draw robot body
        self.canvas.create_rectangle(
            self.robot_x, self.robot_y, 
            self.robot_x + self.robot_length, self.robot_y + self.robot_height, 
            outline='black', fill='grey'
        )
        # Draw shooter wheel with rotating markings
        self.canvas.create_oval(
            self.shooter_center[0] - self.shooter_radius, self.shooter_center[1] - self.shooter_radius,
            self.shooter_center[0] + self.shooter_radius, self.shooter_center[1] + self.shooter_radius,
            outline='black', fill='red'
        )
        # Shooter wheel marking
        mark_x = self.shooter_center[0] + self.shooter_radius * math.cos(self.shooter_mark_angle)
        mark_y = self.shooter_center[1] + self.shooter_radius * math.sin(self.shooter_mark_angle)
        self.canvas.create_line(
            self.shooter_center[0], self.shooter_center[1],
            mark_x, mark_y,
            fill='black', width=2
        )

        # Draw hood arc
        hood_angle_rad = math.radians(self.hood_angle)
        hood_x = self.shooter_center[0] + (self.shooter_radius + self.ball_diameter / 2) * math.sin(hood_angle_rad)
        hood_y = self.shooter_center[1] - (self.shooter_radius + self.ball_diameter / 2) * math.cos(hood_angle_rad)
        self.canvas.create_arc(
            self.shooter_center[0] - self.shooter_radius - self.ball_diameter / 2, 
            self.shooter_center[1] - self.shooter_radius - self.ball_diameter / 2,
            self.shooter_center[0] + self.shooter_radius + self.ball_diameter / 2,
            self.shooter_center[1] + self.shooter_radius + self.ball_diameter / 2,
            start=90, extent=self.hood_angle, 
            outline='black', style=tk.ARC, width=2
        )

        # Draw ball
        if self.ball_visible:
            ball_x, ball_y = self.ball_position
            self.canvas.create_oval(
                ball_x - self.ball_diameter / 2, ball_y - self.ball_diameter / 2,
                ball_x + self.ball_diameter / 2, ball_y + self.ball_diameter / 2,
                outline='black', fill='orange'
            )

    def _draw_goal(self):
        goal_color = 'yellow' if self.goal_lit_up else 'darkgrey'
        self.canvas.create_rectangle(
            self.goal_x - self.goal_width / 2, self.goal_center_y - self.goal_height / 2,
            self.goal_x + self.goal_width / 2, self.goal_center_y + self.goal_height / 2,
            outline='black', fill=goal_color
        )

    def set_shooter_speed(self, speed):
        """Set the shooter wheel speed in radians per second."""
        self.shooter_wheel_speed = speed

    def set_hood_extension(self, angle):
        """Set the hood angle in degrees from vertical."""
        self.hood_angle = angle

    def set_ball_position(self, x, y, visible=True):
        """Set the ball's position and visibility."""
        self.ball_position = (x, y)
        self.ball_visible = visible

    def set_goal_position(self, y):
        """Set the vertical position of the goal."""
        self.goal_center_y = y

    def set_goal_lit_up(self, lit_up):
        """Set whether the goal is lit up."""
        self.goal_lit_up = lit_up

    def _animate(self):
        """Animate the visualization, including rotating the shooter wheel."""
        while self.running:
            self.canvas.delete("all")  # Clear the canvas
            self._draw_robot()
            self._draw_goal()
            # Rotate the shooter wheel marking
            self.shooter_mark_angle += self.shooter_wheel_speed * 0.05  # Adjust the speed and time factor
            time.sleep(0.05)  # Refresh rate

    def start(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def stop(self):
        """Stop the animation and close the window."""
        self.running = False
        self.animation_thread.join()
        self.root.destroy()

# Example usage:
if __name__ == "__main__":
    viz = Visualization()
    viz.set_shooter_speed(25)  # Set shooter wheel speed in radians per second
    viz.set_hood_extension(130)  # Extend hood to 45 degrees
    viz.set_ball_position(300, 200, True)  # Set ball position and make it visible
    viz.set_goal_position(180)  # Adjust goal position
    viz.set_goal_lit_up(False)  # Light up the goal
    viz.start()  # Start the visualization
