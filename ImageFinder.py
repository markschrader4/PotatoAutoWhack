from PIL import ImageGrab
from win32api import GetSystemMetrics
from cv2 import imread, IMREAD_GRAYSCALE, ORB_create, cvtColor, COLOR_RGB2GRAY
from cv2 import BFMatcher, NORM_HAMMING
from numpy import array


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
        self.screen = ImageGrab.grab(bbox=(self.screenStartx, self.screenStarty,
                                      self.screenEndx, self.screenEndy))
        
    def get_ref_kp_and_des(self):
        """Returns keypoints and descriptors of gray refImage.
        """
        grayRefImage = imread(self.refImage, IMREAD_GRAYSCALE)
        return ORB_create().detectAndCompute(grayRefImage, None)
    
    def get_screen_kp_and_des(self):
        """Returns keypoints and descriptors of gray screen.
        """
        gray_screen = cvtColor(array(self.screen), COLOR_RGB2GRAY)
        return ORB_create().detectAndCompute(gray_screen, None)
    
    def update_screen(self):
        """Sets screen to what is currently on screen
        """
        self.screen = ImageGrab.grab(bbox=(self.screenStartx, self.screenStarty,
                                      self.screenEndx, self.screenEndy))
    
    def brute_force_match(self):
        """Returns descriptor and keypoint matches, sorted by distance.
        """
        bf = BFMatcher(NORM_HAMMING, crossCheck=True)
        kp_ref, des_ref = self.get_ref_kp_and_des()
        kp_scrn, des_scrn = self.get_screen_kp_and_des()
        return sorted(bf.match(des_ref, des_scrn), key = lambda x:x.distance)