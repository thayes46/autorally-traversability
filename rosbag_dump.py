#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dump relevant contents of rosbag file into numpy arrays
"""

import rosbag
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

fpath = '/Users/thomas.king/Downloads/'
fname = '2020-09-14-14-35-43_0.bag'

# Open bag
bag = rosbag.Bag(fpath + fname)

# Print out topics if needed
topics = bag.get_type_and_topic_info()[1].keys()

#%% Coord transform between chassis and camera frame
numsg = 1;
for topic, msg, t in bag.read_messages(topics=['/tf_static']):
    # print(msg)
    numsg -= 1
    if numsg < 1:
        break
    
T = np.array([[msg.transforms[1].transform.translation.x,
               msg.transforms[1].transform.translation.y,
               msg.transforms[1].transform.translation.z]])

#%% Camera Intrinsic Matrix
numsg = 1
for topic, msg, t in bag.read_messages(topics=['/left_camera/camera_info']):
    # print(msg)
    numsg -= 1
    if numsg < 1:
        break
K = np.reshape(msg.K,(3,3))

#%% Vehicle pose in world frame
x = y = z = time = np.array([])

for topic, msg, t in bag.read_messages(topics=['/ground_truth//state_raw']):
    time = np.append(time,msg.header.stamp.to_time())
    x = np.append(x,msg.pose.pose.position.x)
    y = np.append(y,msg.pose.pose.position.y)
    z = np.append(z,msg.pose.pose.position.z)

# Plot vehicle pose in world frame
ax = plt.axes(projection='3d')
ax.plot3D(x,y,z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Vehicle Pose in World Frame')

bag.close()

