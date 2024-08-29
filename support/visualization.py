import tkinter as tk
import math

class Visualization:
    def __init__(self):
        # Initialize the main window and canvas
        self.root = tk.Tk()
        self.root.title("FRC Robot Visualization")
        self.canvas_width = 800
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, bg='white', width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Robot parameters
        self.robot_length = 100
        self.robot_height = 60
        self.robot_x = 50
        self.robot_y = 350
        self.shooter_radius = 15
        self.shooter_center = (self.robot_x + self.robot_length, self.robot_y)
        self.shooter_wheel_speed = 0  # radians per second
        self.shooter_mark_angle = 0  # Initial angle for shooter wheel marking
        self.hood_angle = 0  # Hood extension in degrees from vertical

        # Ball parameters
        self.ball_diameter = 15
        self.ball_position = (self.robot_x, self.robot_y)
        self.ball_visible = False

        # Goal parameters
        self.goal_x = self.robot_x + 5 * self.robot_length
        self.goal_center_y = 200
        self.goal_width = 40
        self.goal_height = 120
        self.goal_lit_up = False

        # Scoring and time display
        self.score = 0
        self.time_remaining = 120  # seconds


        # Set the close flag
        self.window_closed = False
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # Start the animation
        self.running = True
        self._animate()  # Use after() method instead of while loop

    def _draw_floor(self):
        """Draw the floor and the air division line."""
        self.canvas.create_rectangle(
            0, self.robot_y, self.canvas_width, self.canvas_height,
            fill='grey', outline='grey'
        )
        self.canvas.create_line(
            0, self.robot_y, self.canvas_width, self.robot_y,
            fill='black'
        )

    def _draw_robot(self):
        """Draw the robot with a shooter wheel, hood, and bumper."""
        # Draw robot body
        self.canvas.create_rectangle(
            self.robot_x, self.robot_y - self.robot_height,
            self.robot_x + self.robot_length, self.robot_y,
            fill='tan'
        )

        # Draw robot bumper with team number
        self.canvas.create_rectangle(
            self.robot_x - 10, self.robot_y - 10,
            self.robot_x + self.robot_length + 10, self.robot_y,
            fill='red'
        )
        self.canvas.create_text(
            self.robot_x + self.robot_length / 2, self.robot_y - 5,
            text="1736", fill="white", font=("Arial", 10)
        )

        # Draw shooter wheel with rotating markings
        self.shooter_center = (self.robot_x + self.robot_length, self.robot_y - self.robot_height)
        self.canvas.create_oval(
            int(self.shooter_center[0] - self.shooter_radius), 
            int(self.shooter_center[1] - self.shooter_radius),
            int(self.shooter_center[0] + self.shooter_radius), 
            int(self.shooter_center[1] + self.shooter_radius),
            fill='red'
        )

        # Shooter wheel markings
        mark_x = self.shooter_center[0] + self.shooter_radius * math.cos(self.shooter_mark_angle)
        mark_y = self.shooter_center[1] + self.shooter_radius * math.sin(self.shooter_mark_angle)
        self.canvas.create_line(
            int(self.shooter_center[0]), int(self.shooter_center[1]),
            int(mark_x), int(mark_y),
            fill='white', width=2
        )
        mark_x = self.shooter_center[0] + self.shooter_radius * math.cos(self.shooter_mark_angle+math.pi/2.0)
        mark_y = self.shooter_center[1] + self.shooter_radius * math.sin(self.shooter_mark_angle+math.pi/2.0)
        self.canvas.create_line(
            int(self.shooter_center[0]), int(self.shooter_center[1]),
            int(mark_x), int(mark_y),
            fill='black', width=2
        )

        mark_x = self.shooter_center[0] + self.shooter_radius * math.cos(self.shooter_mark_angle+math.pi)
        mark_y = self.shooter_center[1] + self.shooter_radius * math.sin(self.shooter_mark_angle+math.pi)
        self.canvas.create_line(
            int(self.shooter_center[0]), int(self.shooter_center[1]),
            int(mark_x), int(mark_y),
            fill='black', width=2
        )

        mark_x = self.shooter_center[0] + self.shooter_radius * math.cos(self.shooter_mark_angle+math.pi*3.0/2.0)
        mark_y = self.shooter_center[1] + self.shooter_radius * math.sin(self.shooter_mark_angle+math.pi*3.0/2.0)
        self.canvas.create_line(
            int(self.shooter_center[0]), int(self.shooter_center[1]),
            int(mark_x), int(mark_y),
            fill='black', width=2
        )

        # Draw hood arc
        self.canvas.create_arc(
            int(self.shooter_center[0] - self.shooter_radius - self.ball_diameter / 2), 
            int(self.shooter_center[1] - self.shooter_radius - self.ball_diameter / 2),
            int(self.shooter_center[0] + self.shooter_radius + self.ball_diameter / 2),
            int(self.shooter_center[1] + self.shooter_radius + self.ball_diameter / 2),
            start=180, extent=-self.hood_angle - 90, 
            outline='black', style=tk.ARC, width=2
        )

        # Draw ball
        if self.ball_visible:
            ball_x, ball_y = self.ball_position
            self.canvas.create_oval(
                int(ball_x - self.ball_diameter / 2), 
                int(ball_y - self.ball_diameter / 2),
                int(ball_x + self.ball_diameter / 2), 
                int(ball_y + self.ball_diameter / 2),
                fill='orange'
            )

    def _draw_goal(self):
        """Draw the goal with the ability to light it up."""
        goal_color = 'yellow' if self.goal_lit_up else 'darkgrey'
        self.canvas.create_rectangle(
            int(self.goal_x - self.goal_width / 2), 
            int(self.goal_center_y - self.goal_height / 2),
            int(self.goal_x + self.goal_width / 2), 
            int(self.goal_center_y + self.goal_height / 2),
            fill=goal_color
        )

        # Draw score and time
        self.canvas.create_text(self.canvas_width // 2, 20, text=f"Score: {self.score}", font=("Arial", 16))
        self.canvas.create_text(self.canvas_width // 2, 40, text=f"Time Remaining: {self.time_remaining:6.2f}s", font=("Arial", 16))


    def set_shooter_speed(self, speed):
        """Set the shooter wheel speed in radians per second."""
        self.shooter_wheel_speed = speed * 0.1 #hack 

    def set_hood_extension(self, angle):
        """Set the hood angle in degrees from horizontal."""
        self.hood_angle = angle

    def set_ball_position(self, x, y, visible=True):
        """Set the ball's position and visibility."""
        y = self.robot_y - y
        self.ball_position = (int(x), int(y))
        self.ball_visible = visible

    def set_goal_position(self, y):
        """Set the vertical position of the goal."""
        y = self.robot_y - y
        self.goal_center_y = y

    def set_goal_lit_up(self, lit_up):
        """Set whether the goal is lit up."""
        self.goal_lit_up = lit_up
        
    def set_score(self, score):
        self.score = score

    def set_time_remaining(self, time_seconds):
        self.time_remaining = time_seconds
    

    def is_window_open(self):
        """Check if the visualization window is still open."""
        return not self.window_closed

    def _animate(self):
        """Animate the visualization, including rotating the shooter wheel."""
        if not self.running:
            return
        
        self.canvas.delete("all")  # Clear the canvas
        self._draw_floor()
        self._draw_robot()
        self._draw_goal()

        # Rotate the shooter wheel marking
        self.shooter_mark_angle += self.shooter_wheel_speed * 0.05  # Adjust speed and time factor

        self.canvas.after(20, self._animate)  # Schedule next animation frame

    def start(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()

    def stop(self):
        """Stop the animation and close the window."""
        self.running = False
        self.root.destroy()

    def _on_close(self):
        """Handle window close event."""
        self.window_closed = True
        self.stop()

# Example usage:
if __name__ == "__main__":
    viz = Visualization()
    viz.set_shooter_speed(2)  # Set shooter wheel speed in radians per second
    viz.set_hood_extension(60)  # Extend hood to 45 degrees
    viz.set_ball_position(300, 200, True)  # Set ball position and make it visible
    viz.set_goal_position(180)  # Adjust goal position
    viz.set_goal_lit_up(True)  # Light up the goal
    viz.start()  # Start the visualization
