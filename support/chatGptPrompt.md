I'm looking to describe a graphical visualization that need to be implemented in python, with minimal to no additional installations (I believe tk is built in?) It should be drawn on a canvas which appears when the visualization is started.

The overall visualiztion will show a FRC First Robotics robot's side view, as it sits on the playing field and shoots into a goal. It will all be a 2d visualization. Simple block/outline representations of the components is fine, but different colors should be used to differentiate components.

The visualization should be implemented inside a single class, with API's to set properties of how it looks per below. It should have a method which animates the drawing asynchronously in the background. The class shall be named `Visualization`.

"X" is horizontal along the ground, increasing left to right. Y is vertical in the air, increasing from bottom to top. The robot's base shall be at the origin.

The visualization should have the following:

1) a stationary FIRST robotics robot, with a small shooter wheel that launches balls. There should be an API to set the rotational speed of the shooter wheel in radians per second. The small shooter wheel should have markings that visually rotate on it when being animated at the specified speed in radians per second. The robot should have a red "bumper" slightly longer than itself near the floor, with the number 1736 written on it.
2) The "hood" - A black semi-circle over the top of the shooter wheel that forms the "hood", constraining the ball until it is released. It should be one ball width away from the shooter wheel. There should be an API for setting how far extended the hood is. The input should be in units of degrees away from vertical (where 0 degrees is "ends over the top of the shooter").  This arc should be drawn to start a the Y coordinate of the shooter wheel circle, and extend to the angle specified by the input API. To be clear, as the value to the API increases, the hood should grow from the left side of the shooter wheel, up over the top toward the right side.
3) a ball that can be placed at any x/y coordinate, and can be selected to be visible or not.
4) A "goal" of a fixed size, at a fixed X coordinate that is visually about 5x the robot's length away from the robot, and with an API to adjust its center location in the Y direction. I will write code to call this api to supply the vertical position.
5) An additional API for the goal which causes it to "light up" and be a brighter color, or be darker and not lit up.
6) The floor should be grey colored, the background ("air") may be white. A black line at Y=0 should divide the "floor" (y<0) from the "air" (y>0)

Finally, there should be an API to determine if the user has closed the window and it is no longer visible.

The view window only needs to go down to about -10 in the Y dimension. Pick the upper limit for Y and both x limits to allow some margin around the drawn objects, but we don't need a ton.

Be sure to avoid flickering. Double-buffering and swapping the visible frame in a single call (rather than clearing and redrawing) is a good technique.

Remember tkinter can only take `int` types for inputs of pixel coordiantes - be sure all pixel coordinate calcualtions use `int` or `round` or something similar to convert.
