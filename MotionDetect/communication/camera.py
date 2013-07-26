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
        self.lastAskedPosition = "hold"

    def isOn(self):
        print "---"
        
    def isMoving(self):
        return self.moving
        
    def turnOn(self):
        print "---"
        
    def turnOff(self):
        print "---"
    
    def move(self, direction):
        if( direction == 'left' ):
            self.moveLeft(1)
        if( direction == 'right'):
            self.moveRight(1)
        if( direction == 'hold' ):
            self.hold(1)

    def moveLeft(self, steps):
        if( self.lastAskedPosition == "left"):	
            self.log.info("Movendo a camera para esquerda")
            return
        if( not self.move_(steps, "left") ):
            self.log.warning("Impossível mover a câmera para esquerda...")            
        self.log.info("Movendo a camera para esquerda")
        self.lastAskedPosition = "left"
        
    def moveRight(self, steps):
        if( self.lastAskedPosition == "right"):	
            self.log.info("Movendo a camera para direita")
            return
        if( not self.move_(steps, "right") ):
            self.log.warning("Impossível mover a câmera para direita...")            
        self.log.info("Movendo a camera para direita")
        self.lastAskedPosition = "right"
    
    def hold(self, steps):
        if ( self.lastAskedPosition == "hold" ) :
            self.log.info("Parando o movimento da camera")
            return
        if( not self.move_(steps, "hold") ):
            self.log.warning("Impossível hold")            
        self.log.info("Parando o movimento da camera")     
        self.lastAskedPosition = "hold" 
    '''
    Post action
    '''
    def move_(self,steps, diraction):  
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
        return True      
        
    def canMoveRight(self):
        return True
    
