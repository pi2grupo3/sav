#coding: utf-8-

'''
@autor: Eusyar Alves de Carvalho
@contact: eusyar
Versão 0.0.2
'''

import cv2.cv as cv
import cv2

from utils.generic import ut
from utils.generic import log
from utils.booter import Boot

from algorithm.hmt import HMT
   
if __name__ == "__main__":    
    
    # boot
    conf = Boot()
    conf.disclamer()      

    log = log(conf.getProperty("log_file"))
    log.info( "Preparando o programa... ")
    
    cam_rec = ut.cam(conf.getProperty("src_movie"))
    
    log.info( "Programa iniciado com sucesso ")
    
    hmt = HMT(cam_rec, conf, log)
    
    while ( ut.running() ):   
        img = hmt.run()
        cv2.imshow('Image', img)
    
    conf.freeCamera(cam_rec)
    
    log.info( "Programa finalizado com sucesso ")
