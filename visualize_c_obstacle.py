'''
visualize_c_obstacle.py

Visualize the 2D (translational) configuration space obstacle. The program provides two animations.
One shows the 2D configuration space obstacle as the trajectory of the robot at all 
of its colliding position with the original obstacle. The other shows how the configuratioin space obstacle
can be found by offsetting the flipped robot (around the reference point) with the obstacle (Minskowski sum). 

The resulted C-obstacle and the reference point reduces the 2D motion planning
problem with convex polygonal robot and obstacle to 1D with point robot and 
convex polygonal obstacle, which can be solved effectively with visibility graph and 
path finding algorithm.


Jackie Zhong (jackie.z@wustl.edu)

Last Edited: 12/30/21

References
    https://stackoverflow.com/questions/38341722/animation-to-translate-polygon-using-matplotlib
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.ConvexHull.html
'''

####################  Program Configuration ###########################
'''
Change variables in this section to configure the program behaviour:

    - raw_obstacle_points: 2D points representing a obstacle. The program
      forces the obstacle to be convex by constructing the convex hull
      using these points
    
    - raw_robot_points: 2D points representing the robot. The program
      forces the robot to be convex by constructing the convex hull
      using these points

    - step_size: determine the size of step of the robot travelling around
      the c-obstacle, also determine how many frames are there 

    - interval: interval between each frame of animation

    - margin: how spacefull will the view range be
'''

# robot and obstacle points
raw_obstacle_points = [ [4, 2], [7, 4], [6, -2], [8, 0] ]
raw_robot_points = [ [-1, -1], [0, 2], [1, -1]]

# animation control
interval = 70
step_size = 25
margin = 2

##########################################################################


import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull, convex_hull_plot_2d
from matplotlib import animation
import matplotlib.patches as patches

'''
    Parse options
'''
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-f", "--flipped", action="store_true", dest="flipped", default=False)
(options, args) = parser.parse_args()

'''
    force the obstacle to be convex
'''
obstacle_hull = ConvexHull(raw_obstacle_points)
obstacle_points = []
for i in obstacle_hull.vertices:
    obstacle_points.append(raw_obstacle_points[i])

'''
    Process robot to reposition at origin and 
    flip around the origin
'''

# force robot to be a convex shape
robot_hull = ConvexHull(raw_robot_points)
robot_points = []
for i in robot_hull.vertices:
    robot_points.append(raw_robot_points[i])


# reposition robot to let its first point be at (0,0) and flip it
translate_x = 0 - robot_points[0][0]
translate_y = 0 - robot_points[0][1]

robot_left_most = 0
robot_right_most = 0
robot_top_most = 0
robot_bottom_most = 0

repositioned_robot_points = []
for point in robot_points:
        x = point[0] + translate_x
        y = point[1] + translate_y

        robot_left_most = min(robot_left_most, x)
        robot_right_most = max(robot_right_most, x)
        robot_top_most = max(robot_top_most, y)
        robot_bottom_most = min(robot_bottom_most, y)

        repositioned_robot_points.append([-x,-y])


'''
    Find C-obstacle using minskowsi sum of
    convex hulls
'''

# minskowski sum of convex hulls
minskowsi_sum = []
for p in repositioned_robot_points:
    for q in obstacle_points:
        x = p[0] + q[0]
        y = p[1] + q[1]
        minskowsi_sum.append([x,y])

minskowski_hull = ConvexHull(minskowsi_sum)

c_obstacle_points = []
for i in minskowski_hull.vertices:
    c_obstacle_points.append(minskowsi_sum[i])


'''
    reposition robot to prepare for animation
'''

# find extreme points in the convex hull of c-obstacle
c_left_most_x = c_obstacle_points[0][0] 
c_left_most_y = c_obstacle_points[0][1] 
c_right_most_x = c_obstacle_points[0][0]
c_right_most_y = c_obstacle_points[0][1]

c_top_most_y = c_obstacle_points[0][1]
c_bottom_most_y = c_obstacle_points[0][1]

for point in c_obstacle_points:
    if point[0] < c_left_most_x:
        c_left_most_x = point[0]
        c_left_most_y = point[1]
    elif point[0] > c_right_most_x:
        c_right_most_x = point[0]
        c_right_most_y = point[1]

    if point[1] > c_top_most_y:
        c_top_most_y = point[1]
    elif point[1] < c_bottom_most_y:
        c_bottom_most_x = point[0]
        c_bottom_most_y = point[1]

# find extreme points in the convex hull of original obstacle
left_most_x = obstacle_points[0][0] 
left_most_y = obstacle_points[0][1] 
right_most_x = obstacle_points[0][0]
right_most_y = obstacle_points[0][1]

top_most_y = obstacle_points[0][1]
bottom_most_y = obstacle_points[0][1]

for point in obstacle_points:
    if point[0] < left_most_x:
        left_most_x = point[0]
        left_most_y = point[1]
    elif point[0] > right_most_x:
        right_most_x = point[0]
        right_most_y = point[1]

    if point[1] > top_most_y:
        top_most_y = point[1]
    elif point[1] < bottom_most_y:
        bottom_most_y = point[1]

# depending on animation type, set different position
tmp_robot_points, tmp_obstacle_points = [], []
tmp_left_most_x, tmp_left_most_y, tmp_right_most_y, tmp_right_most_x = 0, 0, 0, 0
if options.flipped:
    tmp_robot_points = repositioned_robot_points
    tmp_obstacle_points = obstacle_points
    tmp_left_most_x = left_most_x
    tmp_left_most_y = left_most_y
    tmp_right_most_x = right_most_x
    tmp_right_most_y = right_most_y
else:
    tmp_robot_points = robot_points
    tmp_obstacle_points = c_obstacle_points
    tmp_left_most_x = c_left_most_x
    tmp_left_most_y = c_left_most_y
    tmp_right_most_x = c_right_most_x
    tmp_right_most_y = c_right_most_y

# reposition robot to let it collide with obstacle
translate_x = tmp_left_most_x - tmp_robot_points[0][0]
translate_y = tmp_left_most_y - tmp_robot_points[0][1]
animation_robot_points = []
for point in tmp_robot_points:
    x = point[0] + translate_x
    y = point[1] + translate_y
    animation_robot_points.append([x,y])

'''
    Calculate clockwise path along original obstacle
'''

# find the slope of line that separates upper and lower hull
slope = (tmp_right_most_y - tmp_left_most_y) / (tmp_right_most_x - tmp_left_most_x)
y_intercept = tmp_left_most_y - (slope * tmp_left_most_x)

animation_path = []
upper_hull_points = []
lower_hull_points = []
for point in tmp_obstacle_points:
    if point[1] >= (point[0] * slope + y_intercept): 
        upper_hull_points.append(point)
    else:
        lower_hull_points.append(point)

upper_hull_points.sort()
lower_hull_points.sort()
lower_hull_points.reverse()

# construct the location displacement between each frame
animation_points = []
prev_point = upper_hull_points[0]
for point in upper_hull_points:
    if point == upper_hull_points[0]:
        continue
    for i in range(0, step_size):
        animation_points.append([(point[0] - prev_point[0]) / step_size, (point[1] - prev_point[1]) / step_size])
    prev_point = point

for point in lower_hull_points:
    for i in range(0, step_size):
        animation_points.append([(point[0] - prev_point[0]) / step_size, (point[1] - prev_point[1]) / step_size])
    prev_point = point

# going back to starting point
for i in range(0, step_size):
    animation_points.append([(upper_hull_points[0][0] - prev_point[0]) / step_size, (upper_hull_points[0][1] - prev_point[1]) / step_size])


'''
    Prepare for animation
'''

fig = plt.figure()
ax = fig.add_subplot()

# set view range
ax.set_xlim(c_left_most_x + robot_left_most - margin, c_right_most_x + robot_right_most + margin)
ax.set_ylim(c_bottom_most_y + robot_bottom_most - margin, c_top_most_y + robot_top_most + margin)

reference_point, = ax.plot(animation_robot_points[0][0], animation_robot_points[0][1], 'r*')

animation_robot = patches.Polygon(animation_robot_points, ec='red', facecolor="none")
c_obstacle = plt.Polygon(c_obstacle_points, ec='b', facecolor="none")
repositioned_robot = patches.Polygon(repositioned_robot_points, ec='r', facecolor="none")
original_obstacle = patches.Polygon(obstacle_points, ec='black', facecolor="none")


ax.add_patch(c_obstacle)
ax.add_patch(original_obstacle)
ax.add_patch(animation_robot)

# animation function 
def init():
    animation_robot.set_xy(animation_robot_points)
    return animation_robot, reference_point

def animate(i):
    for point in animation_robot_points:
        point[0] += animation_points[i][0]
        point[1] += animation_points[i][1]

    reference_point.set_data(animation_robot_points[0][0], animation_robot_points[0][1])

    animation_robot.set_xy(animation_robot_points)
    return animation_robot,reference_point

ani = animation.FuncAnimation(fig, animate, len(animation_points), init_func=init,
                              interval=interval, blit=False, repeat=True)

plt.show()

