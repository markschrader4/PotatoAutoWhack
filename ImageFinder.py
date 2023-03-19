from PIL import ImageGrab
from win32api import GetSystemMetrics
import cv2 as cv
import numpy as np

class ImageFinder:
    """Matches keypoints from a reference image to the screen
    """
    def __init__(self, refImage, numMatches=10, screenStartx=0, screenStarty=0,
                 screenEndx = GetSystemMetrics(1),
                 screenEndy = GetSystemMetrics(0)):
        self.refImage = refImage
        self.numMatches  = numMatches
        self.screenStartx = screenStartx
        self.screenStarty = screenStarty
        self.screenEndx = screenEndx
        self.screenEndy = screenEndy
        
        self.grayRefImage = cv.imread(self.refImage, cv.IMREAD_GRAYSCALE)
        self.screen = ImageGrab.grab(bbox=(self.screenStartx, self.screenStarty,
                                      self.screenEndx, self.screenEndy))
        
    def get_ref_kp_and_des(self):
        """Returns keypoints and descriptors of refImage.
        """
        return cv.ORB_create().detectAndCompute(self.grayRefImage, None)
    
    def get_screen_kp_and_des(self):
        """Returns keypoints and descriptors of screen.
        """
        gray_screen = cv.cvtColor(np.array(self.screen), cv.COLOR_RGB2GRAY)
        return cv.ORB_create().detectAndCompute(gray_screen, None)
    
    def update_screen(self):
        """Sets screen to what is currently on screen
        """
        self.screen = ImageGrab.grab(bbox=(self.screenStartx, self.screenStarty,
                                      self.screenEndx, self.screenEndy))
    
    def brute_force_match(self):
        """Returns descriptor and keypoint matches, sorted by distance.
        """
        bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
        kp_ref, des_ref = self.get_ref_kp_and_des()
        kp_scrn, des_scrn = self.get_screen_kp_and_des()
        
        return sorted(bf.match(des_ref, des_scrn), key = lambda x:x.distance)