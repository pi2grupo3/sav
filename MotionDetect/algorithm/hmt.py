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
        
        #self.cam_com.moveLeft(5)
        self.cam_com.moveRight(5)
        #self.cam_com.hold(2)
        sys.exit()
        
        #print self.cam_com.ask()
        
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
            #Multiplos alvos para centralizar
            if( len(self.tracker.targets) > 1):
                extremePoints = self.extremePoints()
                ut.drawRect(extremePoints, img, (0, 255, 0) )
            #apenas um alvo para centralizar    
            #else:                
            
            self.tracker.traceTargets(img)                                            
        #ut.draw_str(img, (20, 20), "FPS: " + str(  fps.update()  ) )
        #ut.draw_str(img, (20, 50), "Data: " + str( fps.time()  ) )
        
        # Center Point debug
        #ut.drawRect((0,0, self.w-1, self.h-1), img, (0, 255, 0) )
         
        return img            

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
            
        