#coding: utf-8-

from algorithm.peopledetect import PedestrianDetect
from algorithm.motion import MotionTrack

from communication.camera import CameraCommunicator

from utils.generic import FPS
from utils.generic import ut
from utils.generic import log

import sys

'''
Created on 05/06/2013

@author: eusyar
'''

class HMT:  
    '''
    Classe responsável por juntar os algoritimos de HOG e MOSSE
    '''


    def __init__(self, cam_rec, conf, log):
        self.conf = conf
        self.log = log
        self.pd = PedestrianDetect(padding=(12,12))
        self.cam_com = CameraCommunicator( self.log, self.conf.getProperty("url_server"),"127.0.0.1")
        self.tracker = MotionTrack()
        self.fps = FPS()
        self.cam_rec = cam_rec
        self.time_counter = 0
        
        rval, img = ut.query(self.cam_rec)  
        self.h, self.w = img.shape[:2]
        
        self.center_point = self.w/2 , self.h/2
        cX, cY = self.center_point
        
        x1,y1 = cX - self.w*0.2, cY - self.h*0.2
        x2,y2 = cX + self.w*0.2, cY + self.h*0.2 
        
        self.center_rect = x1,y1,x2,y2
        self.direction = "hold"
       
        #self.cam_com.moveRight(1)
        #self.cam_com.moveLeft(1)
        #sys.exit()

    def run(self):                                            
        self.time_counter += 1
        
        #Mesmo que não exista processamento, é necessário enviar a imagem para ser armazenada
        rval, img = ut.query(self.cam_rec)           
        if(self.time_counter % 40 == 0):                                                        
            if( self.tracker.hasTargets() ):       
                
                print "Reading new targets"
                maybe_targets = self.pd.run(img)   
                real_targets = self.tracker.targets                                
                
                for target_found in maybe_targets:
                    doIt = True
                    for real_target in real_targets:                        
                        if( ut.insindeTwoPoint(target_found, real_target.returnRectPoints(), 200) ):
                            doIt = False
                        else:                            
                            doIt = doIt and True
                    if(doIt):
                        print 'Novo alvo'
                        self.tracker.addTarget(target_found, img)
                
            #Procura novas pessoas no video, caso a camera estiver sem alvos                
            else: 
                print "No targets -- Reading new targets"
                targets = self.pd.run(img)
                if( len(targets) > 0 ):                                        
                    self.tracker.setTargets(targets,img)
        
        if( self.tracker.hasTargets() ):                       
            extremePoints = self.extremePoints()
            centerPoint = self.centerPoint(extremePoints)           
            ut.drawRect(extremePoints, img, (0, 255, 0) )
            if( not ut.pointInsideRect(self.center_rect, centerPoint ) ):
                direction = self.askDirection(centerPoint)
                if( direction != self.direction  ):
                    self.direction = direction
                    if(direction == "right"):
                        self.cam_com.moveRight(1)
                    if(direction == "left"):
                        self.cam_com.moveLeft(1)
                    if(direction == "hold"):
                        self.cam_com.hold(1)            
            self.tracker.traceTargets(img)                                            
       
        else:
            if(self.direction != "hold" ):
                self.direction = "hold"
                self.cam_com.hold(1)


        #ut.draw_str(img, (20, 20), "FPS: " + str(  fps.update()  ) )
        #ut.draw_str(img, (20, 50), "Data: " + str( fps.time()  ) )
        
        # Center Point debug
        ut.drawRect( self.center_rect, img, (255, 0, 0) )
         
        return img            

    def askDirection(self,point):
        x1,y1,x2,y2 = self.center_rect
        xp,yp = point
        if( x1 > xp  ):
            return "left"
        if( x2 < xp ):
            return "right"

        return "hold"

    def extremePoints(self):
        rects = self.tracker.targets
        (tlx,tly), (brx,bry) = (self.w,self.h),(0,0)
        for item in rects:            
            (elx, ely, erx, ery) = item.returnRectPoints()
            if( elx <= tlx):
                (tlx, tly) = (elx, ely)
                        
            if( erx >= brx ):
                (brx, bry) = (erx, ery)
        return tlx,tly, brx,bry

    def centerPoint(self , rect):
        x1,y1,x2,y2 = rect
        return (x1+x2)/2 , (y1+y2)/2
            
    
