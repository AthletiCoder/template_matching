import numpy as np
import cv2
from matplotlib import pyplot as plt
import sys

MIN_MATCH_COUNT = 10

query = cv2.imread(sys.argv[1],0) # query image 
template = cv2.imread(sys.argv[2],0) # template 

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

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = query.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    template = cv2.polylines(template,[np.int32(dst)],True,255,3, cv2.LINE_AA)
else:
    print("Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT))
    sys.exit("Not found")
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

H, W = template.shape
bounds = np.float32([[0,0],[W-1,H-1]]).reshape(-1,1,2)
inv_M, _ = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
rect = cv2.perspectiveTransform(bounds,inv_M)

img3 = cv2.drawMatches(query,kp1,template,kp2,good,None,**draw_params)
p1 = tuple(rect[0][0]) 
p2 = tuple(rect[1][0])
cv2.rectangle(query,p1,p2, (0,0,255),1)
print(p1)
print(p2)
cv2.imwrite('results/found.jpg',query)

cv2.imwrite('results/output.jpg',img3)
