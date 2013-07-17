import cv2.cv as cv
import cv2
from utils.generic import ut 

'''
Created on 26/05/2013
Algoritmo encontrado nos samples 

@author: Eusyar Alves
'''
class PedestrianDetect:
    
    def __init__(self, win_stride=(4,4), padding=(5,5), scale=0.95, group_threshold=1 ):
        self.storage = ut.storage(self)
        self.w_s = win_stride
        self.p = padding
        self.s = scale
        self.g_t = group_threshold               
    
    def inside(self, r, q):
        (rx, ry), (rw, rh) = r
        (qx, qy), (qw, qh) = q
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh
    
    def run(self, frame):
        rects = []
        found = list( cv.HOGDetectMultiScale(cv.fromarray(frame) , self.storage, win_stride=self.w_s,padding=self.p, scale=self.s, group_threshold=self.g_t))
        found_filtered = []
        for r in found:
            insidef = False
            for q in found:
                if self.inside(r, q):
                    insidef = True
                    break
            if not insidef:
                found_filtered.append(r)
        for r in found_filtered:
            (rx, ry), (rw, rh) = r
            #tl = (rx + int(rw*0.1), ry + int(rh*0.07))
            #br = (rx + int(rw*0.9), ry + int(rh*0.87))

            # FIXME!
            print "Antes  do offset " + str(rx) + " " +str(ry) + " - "+str(rx + rw) + "  " + str(ry + rh)
            print "Depois do offset " + str(rx+rw*0.1) + " " +str(ry+rh*0.1) + " - "+ str(rx+rw*0.9) + "  " + str(ry+rh*0.9)

            rects.append( (rx + int(rw*0.1), ry + int(rh*0.1), rx + int(rw*0.9), ry + int(rh*1)) )        
        return rects
        
class FaceDetect:
    
    def __init__(self):
        print '--'
