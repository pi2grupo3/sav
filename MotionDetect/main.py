#coding: utf-8-

'''
Sistema SAV. Ponto de entrada para o programa sav-iprocess, responsavel por criar o 
log, abrir canal de gravação, 'bootar' e manter o loop principal do programa. O processo
de imagem é mantido na classe HMT. 

@autor: Eusyar Alves de Carvalho <eusyar@gmail.com>
@contact: eusyar@gmail.com
@see class htm, log e ut
Versão 0.0.2
'''

import thread
import cv2

from utils.generic import ut
from utils.generic import log
from utils.booter import Boot

from communication.webserver import MyHandler
from mainloop import MainLoopHTTPServer

from algorithm.hmt import HMT

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

if __name__ == "__main__":    
    
    # boot
    conf = Boot()
    conf.disclamer()      

    log = log(conf.getProperty("log_file"))
    log.info( "Preparando o programa... ")

    try:
        log.info("Abrindo o servidor de video")
        server = MainLoopHTTPServer((conf.getProperty("ip"),8080), MyHandler)
        server.init(conf, log)
        
        log.info( "Programa iniciado com sucesso ")        
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()
        log.info( "Programa finalizado com sucesso ")     
    