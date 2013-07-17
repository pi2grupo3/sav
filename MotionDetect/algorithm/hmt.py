#coding: utf-8-

from algorithm.peopledetect import PedestrianDetect
from algorithm.motion import MotionTrack

from communication.camera import CameraCommunicator

from utils.generic import FPS
from utils.generic import ut
from utils.generic import log

from time import time
from datetime import datetime

import sys

'''
Algoritmo responsável por coordenar os demais algoritmos de processamento
de imagens. Essa classe representa a lógica de processamento de imagen para 
uma camera. Utilizando encapsulamento, as chamadas para os algoritmos MOSSE 
e HOG estão simplificadas para o melhor compreendimento. Nesse sentido apenas
as chamadas 'run' e 'traceTargets' precisam ser chamada para atualizar o 
estado dos pedestres detectados.

A descrição está presente no apresenta o fluxo para a detecção de uma câmera:

@autor: Eusyar Alves de Carvalho
@contact: eusyar@gmail.com
@see classe PedestrianDetect, MotionTrack, CameraCommunicator
Versão 0.0.2
'''

class HMT:  

    '''
    Define a entrada da camera com parametro passado, em relação ao 
    arquivo de configurações e com o log passado. Abre uma sessão de
    comunicação com a camera, de detecção de pedestres, e de persegui-
    ção de alvos (no formato de objetos).
    '''
    def __init__(self, cam_rec, conf, log):
        
        #Inicialização dos objetos de auxílio
        self.conf = conf
        self.log = log
        self.fps = FPS()        

        #Inicialização dos algoritimos de detecção
        self.pd = PedestrianDetect(padding=(12,12))
        self.cam_com = CameraCommunicator( self.log, self.conf.getProperty("url_server"),"127.0.0.1")
        self.tracker = MotionTrack()
        
        #Inicialização dos objetos de leitura e escrita de video
        self.cam_rec = cam_rec
        rval, img = ut.query(self.cam_rec)  
        self.h, self.w = img.shape[:2]
        self.filePath = self.conf.getProperty("video_output_dir")
        self.streamOutput = self.conf.getProperty("video_output_stream")
        self.cam_writer = ut.writer(self.cam_rec, self.h, self.w,  self.filePath + ut.timeToFileName() )        
        self.cam_stream = ut.writer(self.cam_rec, self.h, self.w,  self.streamOutput, 'flv', 'flv')

        #Inicialização das variaveis de auxílio
        self.time_counter = 0
        self.time = time()
        self.center_point = self.w/2 , self.h/2
        cX, cY = self.center_point
        
        x1,y1 = cX - self.w*0.2, cY - self.h*0.2
        x2,y2 = cX + self.w*0.2, cY + self.h*0.2 
        
        self.center_rect = x1,y1,x2,y2
        self.direction = "hold"         

        #self.cam_com.moveRight(1)
        #self.cam_com.moveLeft(1)
        #self.cam_com.hold(1) 
        #sys.exit()

    def __del__(self):
        self.cam_writer.release() 

    '''
    Função que executa a lógica do sav. Essa parte executa o caso de uso padrão.
    O código segue o fluxograma apresentado no inicio do código, no entanto alguns
    comentários estão presentes para explicá-lo de maneira mais simples.
    '''
    def run(self):                                            
        self.time_counter += 1
        
        #Verifica se existe a necessidade de criar um novo arquivo de vídeo. Isso é definido apartir do tempo
        if(self.time_counter%20 == 0):
            if(ut.newTime(self.time) is not False):
                self.time = time()
                self.cam_writer.release()
                self.cam_writer = ut.writer(self.cam_rec, self.h, self.w,  self.filePath + ut.timeToFileName())
                print "Um ciclo"

        #Mesmo que não exista processamento, é necessário enviar a imagem para ser armazenada
        rval, img = ut.query(self.cam_rec)           
        self.cam_writer.write(img);
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
                    self.cam_com.move(direction)

            else:
                if( not self.direction == "hold"):
                    self.direction = "hold"
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

        self.cam_stream.write(img)
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
            
    
