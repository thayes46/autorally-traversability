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

bag.close()