#coding: utf-8-

import urllib2 as url
import json
from utils.generic import log 

'''
Created on 26/05/2013

@author: eusyar
'''

class CameraCommunicator():
    
    def __init__(self, log, urlServer = "127.0.0.1", urlRaspberry = "127.0.0.1" ):
        self.moving = False
        self.urlServer = urlServer
        self.urlRaspberry = urlRaspberry
        self.log = log
    
    def isOn(self):
        print "---"
        
    def isMoving(self):
        return self.moving
        
    def turnOn(self):
        print "---"
        
    def turnOff(self):
        print "---"
        
    def moveLeft(self, steps):        
        if( not self.move(steps, "left") ):
            self.log.warning("Impossível mover a câmera para esquerda...")            
        self.log.info("Movendo a camera para esquerda")                 
        
    def moveRight(self, steps):
        if( not self.move(steps, "right") ):
            self.log.warning("Impossível mover a câmera para direita...")            
        self.log.info("Movendo a camera para direita")     
    
    def hold(self, steps):
        if( not self.move(steps, "hold") ):
            self.log.warning("Impossível hold")            
        self.log.info("Movendo a camera para direita")     
    
    '''
    Post action
    '''
    def move(self,steps, diraction):  
        if( diraction == "left" ):        
            if( not self.canMoveLeft() ):
                log.info("Impossível mover a câmera...")            
                return False        
        elif( diraction == "right" ):
            if( not self.canMoveRight() ):
                log.info("Impossível mover a câmera...")            
                return False        
        
        if( diraction == "right" or diraction == "left"  or diraction == "hold"):            
            data = json.dumps({'camera':{"go_to_position":diraction} })
            print data
            req = url.Request(self.urlServer)
            req.add_header('Content-Type', 'application/json')        
            return  url.urlopen(req, data)     
        
        else:
            return False         
           
    
    '''
    Request action
    '''
    def ask(self, path="http://10.42.0.1:3000/cameras/1/translade.json"):
        data = json.load(url.urlopen(path))
        return data
      
    def canMoveLeft(self):
        print "Sera?----"
        return True      
        
    def canMoveRight(self):
        print "Sera?----"
        return True
    
    
     
    
    