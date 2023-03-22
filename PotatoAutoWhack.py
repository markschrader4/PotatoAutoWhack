from cv2 import waitKey, getWindowProperty, imread,IMREAD_GRAYSCALE, drawMatches
from cv2 import DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS, imshow, destroyAllWindows
from Mouse import Mouse
from ImageFinder import ImageFinder
from numpy import array, round
from datetime import timedelta, datetime
from time import sleep
from math import dist


class PotatoAutoWhack:
    
    def __init__(self, delayBetweenWhacks=0.2, threshold=250, 
                 screenStartx=300, screenStarty=200,
                 screenEndx=1010, screenEndy=900,
                 showWindow=True, timer=70):
        self.delayBetweenWhacks = delayBetweenWhacks
        self.threshold = threshold
        self.screenStartx = screenStartx
        self.screenStarty = screenStarty
        self.screenEndx = screenEndx
        self.screenEndy = screenEndy
        self.numMatches = 5
        self.showWindow = showWindow
        self.timer = timer
    
    def start(self):
        Imgfind = ImageFinder('PotatoLarger.jpg', self.numMatches,
                              self.screenStartx, 
                              self.screenStarty, self.screenEndx,
                              self.screenEndy)
        kp1, des1 = Imgfind.get_ref_kp_and_des()
        
        #start timer
        starttime = datetime.now()
        endtime = starttime + timedelta(seconds=self.timer)
        self.timer = endtime - datetime.now()
        
        firstloop = True
        while (waitKey(10) != ord('q')) and (self.timer.seconds > 0):
            Imgfind.update_screen()
            kp2, des2 = Imgfind.get_screen_kp_and_des()
            matches = Imgfind.brute_force_match()
            
            if (self.showWindow):
                # close window if 'x' button used
                try:
                    if(not firstloop):
                        if(getWindowProperty('Screen Capture', 1) == -1):
                            break
                except:
                    break
                
                grayRefImage = imread(Imgfind.refImage, IMREAD_GRAYSCALE)
                final_img = drawMatches(array(grayRefImage), kp1,
                                   array(Imgfind.screen), kp2,
                                   matches[:Imgfind.numMatches], None,
                                   flags=DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                imshow('Screen Capture', final_img)
                firstloop = False
            
            self.click_on_potatoes(kp2, matches, Imgfind)
            self.timer = endtime - datetime.now()
            print(self.timer)
            sleep(self.delayBetweenWhacks)
        self.close()
        
    def click_on_potatoes(self, kp2, matches, Imgfind):
        # click on potato if avg dist between points is small enough
        totalAvgDist = 0
        for i in range(Imgfind.numMatches - 1):
            totalAvgDist += dist(kp2[matches[0].trainIdx].pt,#compare first to all
                                      kp2[matches[i+1].trainIdx].pt)
        if(totalAvgDist < self.threshold):
            print("Moving mouse...")
            Mouse.click(round(kp2[matches[0].trainIdx].pt[0]).astype(int) + 
                        Imgfind.screenStartx,
                        round(kp2[matches[0].trainIdx].pt[1]).astype(int) + 
                        Imgfind.screenStarty)
        
    def close(self):
        print("closing")
        destroyAllWindows()
        
    
if __name__ == "__main__":
    PotatoAutoWhack().start()