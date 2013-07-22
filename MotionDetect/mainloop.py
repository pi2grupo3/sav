#coding: utf-8-

import thread
import cv2

from utils.generic import ut
from utils.generic import log
from utils.booter import Boot

from algorithm.hmt import HMT

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

   
class MainLoopHTTPServer( ThreadingMixIn, HTTPServer ):
    """
    Servidor HTTP para abrigar o loop principal. A utilização de um servidor 
    HTTP é a forma mais simples de se manter o compartilhamento de vídeo para o
    stream através do servidor ruby.
        
    @author: Eusyar Alves de Carvalho <eusyar@gmail.com>
    """
    
    """Variável estática"""    
    output_stream = ut.loadJpg()

    def init(self, conf, log):
        self.conf   = conf
        self.log    = log    
        
        # FIXME: Definir uma lógica para mais de uma câmera 
        
        self.log.info("Configurando o loop principal para a camera numero 1")
        self.cam_rec = ut.cam(self.conf.getProperty("src_movie"))
        self.hmt = HMT(self.cam_rec, self.conf, self.log)    
        
        thread.start_new_thread( self.do_Logic, () )
                
    def do_Logic(self):
        """
        Lógica de aquisição e processamento de imagens
        """        
        while ( ut.running() ):    
            MainLoopHTTPServer.output_stream = img = self.hmt.run()
            cv2.imshow('Image', img)

        ut.freeCamera(cam_rec)    
        
    @staticmethod
    def getOutputStream():
        """
        Retorna output_stream, isso daqui não está nada thread_safe
        """
        return MainLoopHTTPServer.output_stream

    