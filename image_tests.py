"""
Pull image from rosbag and call processing
"""

import rosbag
import numpy as np
from cv_bridge import CvBridge

bridge = CvBridge()
import cv2 as cv

fpath = '/home/todd/autorally/'
fname = '2020-10-15-11-16-39.bag'

# Open bag
bag = rosbag.Bag(fpath + fname)
output_image_index = 0
# Print out topics if needed
topics = bag.get_type_and_topic_info()[1].keys()
for topic, msg, t in bag.read_messages(topics=['/left_camera/image_raw']):
    # Convert image message to OpenCV format
    cv_image = bridge.imgmsg_to_cv2(msg)
    grey_image = cv.cvtColor(cv_image, cv.COLOR_RGB2GRAY)
    # Watershed segmentation used from:
    # https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html

    ret, thresh = cv.threshold(grey_image, 0, 255,
                               cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=2)
    # sure background area
    sure_bg = cv.dilate(opening, kernel, iterations=3)
    # Finding sure foreground area
    dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.7 * dist_transform.max(), 255,
                                0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv.subtract(sure_bg, sure_fg)
    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    # Apply watershed
    markers = cv.watershed(cv_image, markers)
    marker_file = str(output_image_index) + "-markers.png"
    cv.imwrite(marker_file, markers)
    # image was read only for some reason
    cv_image.setflags(write=1)
    cv_image[markers == -1] = [255, 0, 0]
    # display image
    image_file = str(output_image_index) + ".png"
    print("writing to file: ", image_file)
    output_image_index = output_image_index + 1
    cv.imwrite(image_file, cv_image)


bag.close()
