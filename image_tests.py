"""
Pull image from rosbag and call processing
"""

import rosbag
import numpy as np
fpath = '/home/todd/autorally/'
fname = '2020-10-15-11-16-39.bag'

# Open bag
bag = rosbag.Bag(fpath + fname)

# Print out topics if needed
topics = bag.get_type_and_topic_info()[1].keys()
for topic, msg, t in bag.read_messages(topics=['/left_camera/image_raw']):
    print("Height: ", msg.width)
    print("Width: ", msg.height)
    print("encoding", msg.encoding)


bag.close()
