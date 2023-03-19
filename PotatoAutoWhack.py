#ImageFinder test
import cv2 as cv
from Mouse import Mouse
from ImageFinder import ImageFinder
import numpy as np
import math, time

def main():
    delayBetweenWhacks = 0.2
    threshold = 250
    Imgfind = ImageFinder('PotatoLarger.jpg', screenStartx=300, 
                          screenStarty=200, screenEndx=1010,
                          screenEndy=900, numMatches=5)
    kp1, des1 = Imgfind.get_ref_kp_and_des()
    
    while cv.waitKey(10) != ord('q'):
        time.sleep(delayBetweenWhacks)
        Imgfind.update_screen()
        
        kp2, des2 = Imgfind.get_screen_kp_and_des()
        matches = Imgfind.brute_force_match()
        
        grayRefImage = cv.imread(Imgfind.refImage, cv.IMREAD_GRAYSCALE)
        final_img = cv.drawMatches(np.array(grayRefImage), kp1,
                               np.array(Imgfind.screen), kp2,
                               matches[:Imgfind.numMatches], None,
                               flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        cv.imshow('Screen Capture', final_img)
        
        #click on potato if avg dist between points is small enough
        totalAvgDist = 0
        for i in range(Imgfind.numMatches - 1):
            totalAvgDist += math.dist(kp2[matches[0].trainIdx].pt,#compare first to all
                                      kp2[matches[i+1].trainIdx].pt)
        if(totalAvgDist < threshold):
            print("Moving mouse...")
            Mouse.click(np.round(kp2[matches[0].trainIdx].pt[0]).astype(int) + 
                        Imgfind.screenStartx,
                        np.round(kp2[matches[0].trainIdx].pt[1]).astype(int) + 
                        Imgfind.screenStarty)
            
    cv.destroyAllWindows()
    
if __name__ == "__main__":
    main()