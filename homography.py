import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

# https://mybinder.org/v2/gh/ipython/ipython-in-depth/7e5ce96cc9251083979efdfc393425f1229a4a68

MIN_MATCH_COUNT = 30

def resize(img, ratio):
    ret = cv2.resize(img,(0,0),fx=ratio,fy=ratio,interpolation=cv2.INTER_NEAREST)
    return ret

query = cv2.imread(sys.argv[1],0) # query image 
template = cv2.imread(sys.argv[2],0) # template 

query = resize(query,0.2)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(query,None)
kp2, des2 = sift.detectAndCompute(template,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

if len(good)>= MIN_MATCH_COUNT:
    print("Number of matching points: ", len(good))
    print("Match found, check results folder")
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    '''
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = query.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    template = cv2.polylines(template,[np.int32(dst)],True,255,3, cv2.LINE_AA)
    '''
else:
    print("Not enough matching points were found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    sys.exit("Match not found")
    matchesMask = None

# draw_params = dict(matchColor = (0,255,0), singlePointColor = None,matchesMask=matchesMask,flags = 2)
# img3 = cv2.drawMatches(query,kp1,template,kp2,good,None,**draw_params)
# cv2.imwrite('results/output.jpg',img3)

H, W = template.shape
bounds = np.float32([[0,0],[W-1,H-1]]).reshape(-1,1,2)
inv_M, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
rect = cv2.perspectiveTransform(bounds,inv_M)

p1 = tuple(rect[0][0]) 
p2 = tuple(rect[1][0])
cv2.rectangle(query,p1,p2, (0,0,255),1)
# print(p1)
# print(p2)
cv2.imwrite('results/found.jpg',query)
