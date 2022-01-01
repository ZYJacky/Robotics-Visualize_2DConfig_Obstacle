# robotics-visualize-2dConfigObstacle

Visualize the 2D configuration space obstacle in motion planning with convex polygonal robot and obstacle. The program finds the configuration space obstacle by taking advantage of the fact that the convex hull of Minskowski sum is the Minskowski sum of the convex hull (of the robot and obstacle).

## Dependencies

matplotlib, scipy, numpy

## Usage

The program provides two animations. The default one illustrates the configuration space obstacle as the trajectory of the robot at all of its colliding points with the original obstacle. To run, simply issue:

`python visualize_c_obstacle.py`

The other animation seeks to provide some intuition of why the Minskowski sum generates the configuration space obstacle by showing the offsetting of the flipped robot (around a reference point) from the original obstacle. To run, issue:

`python visualize_c_obstacle.py -f`

To customize the robot and obstacle, as well as the animation speed, see the Program Configuration section at the beginning of the .py file. 

## Background Reading
https://www.cs.cmu.edu/~motionplanning/lecture/Chap3-Config-Space_howie.pdf
https://en.wikipedia.org/wiki/Minkowski_addition#Motion_planning



