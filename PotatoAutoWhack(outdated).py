from PIL import ImageGrab
import numpy as np
import cv2 as cv
import time, math
from Mouse import Mouse

# Using keypoints from a reference image, click on closely related
# areas on a larger image. This file was adapted for the game:
# "Farmer Against Potatoes Idle", specifically, the potato whack
# minigame.


# SOURCES: 
# https://www.youtube.com/watch?v=V1DpVjyKTYg
# https://learnopencv.com/edge-detection-using-opencv/
# https://docs.opencv.org/4.5.5/dc/dc3/tutorial_py_matcher.html
# https://amroamroamro.github.io/mexopencv/matlab/cv.ORB.detectAndCompute.html

def main():
    # whack potato area on screen
    startx = 300
    starty = 200
    endx = 1010
    endy = 900
    
    # in seconds
    delayBeforeStart = 5
    delayBetweenWhacks = 0.2
    
    # numMatches and threshold are directly correlated
    numMatches = 5
    threshold = 250
    
    time.sleep(delayBeforeStart)

    # ORB detector + reference image
    img_query = cv.imread('PotatoLarger.jpg', cv.IMREAD_GRAYSCALE)
    orb = cv.ORB_create()

    # find keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img_query, None)

    # BFMatcher object (brute force matcher)
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    while True:
        time.sleep(delayBetweenWhacks)
        # bbox is the whack potato area
        img = ImageGrab.grab(bbox=(startx, starty, endx, endy))
        img_np = np.array(img)
    
        # grayscale
        img_gray = cv.cvtColor(img_np, cv.COLOR_RGB2GRAY)

        # find keypoints and descriptors with ORB
        kp2, des2 = orb.detectAndCompute(img_gray, None)
    
        # match descriptors + sort
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
    
        #click on potato if avg dist between points is small enough
        totalAvgDist = 0
        for i in range(numMatches - 1):
            #print("match", i, kp2[matches[i].trainIdx].pt,#points on training image
            #                  kp1[matches[i].queryIdx].pt)#points on reference image
            totalAvgDist += math.dist(kp2[matches[0].trainIdx].pt,#compare first to all
                                      kp2[matches[i+1].trainIdx].pt)
            #print("\ntotal", totalAvgDist)
        
        
        # click on position if close enough match
        if(totalAvgDist < threshold):
            print("Moving mouse...")
            Mouse.click(np.round(kp2[matches[0].trainIdx].pt[0]).astype(int) + startx,
                       np.round(kp2[matches[0].trainIdx].pt[1]).astype(int) + starty)
        
        # show helper screen - top left picture is reference
        img_final = cv.drawMatches(img_query, kp1, img_gray, kp2,
                               matches[:numMatches], None,
                               flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv.imshow('Screen Capture', img_final)
        
        # q to quit screen capture
        if cv.waitKey(10) == ord('q'):
            break

    cv.destroyAllWindows()
    
if __name__ == "__main__":
    main()