#-----------------------------
# Packages Import
#-----------------------------
import cv2
import numpy as np
import os


#-----------------------------
# Imports a Test Image 
#-----------------------------

current_path= os.path.dirname(__file__)
image_path= os.path.relpath('..\\data\\Test-Knot.jpg', current_path)

FullPathOnLocalMachine= "C:\\Users\\usuario\\Desktop\\Knot-Images-to-regina-code\\data"

print(image_path)
print(FullPathOnLocalMachine)
print (image_path==FullPathOnLocalMachine)
#-----------------------------
# Link Class
#-----------------------------
#This is a class Link it has the following attributes:
# Original_Image - The originial image that is to be analyzed
# FindBorder - List of 4d vectors: A list of the coordinates of blocks arounf the border   
# FindLinkComponent - Function(List of 4d vectors) -> List of lists : Returns the sublist corresponding to the individual link components
# FindCrossing - Function(List of Lists or 4d vectors) -> List of pair of indices: Returns a list of the indices of which lists share a crossing 
# Identify crossing - Function: Uses a small machine learning model to identify whether a corssing is over or under
# ....
class Link:
    # Constructor
    def __init__ (self, image):
        self.original_Image=image
        self.border= self._FindBorder()


    def _FindBorder(self):
        Border=[]
        return Border


