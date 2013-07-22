import string, cgi, time

import algorithm.hmt
from mainloop import MainLoopHTTPServer

from utils.generic import ut

from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn

import re
import cv2, cv

cameraQuality=75

class MyHandler( BaseHTTPRequestHandler  ):

    def do_GET(self):
        global cameraQuality       
        try:
            self.path = re.sub('[^.a-zA-Z0-9]', "", str(self.path))
            if self.path == "" or self.path==None or self.path[:1]==".":
                return
            if self.path.endswith(".html"):
                f = open( curdir + sep + self.path )
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write( f.read()  )
                f.close()
                return
            if self.path.endswith(".mjpeg"):                
                self.send_response(200)
                self.wfile.write("content-Type: multipart/x-mixed-replace; boundary=--aaboundary")
                self.wfile.write("\r\n\r\n")
                while 1:
                    output = MainLoopHTTPServer.getOutputStream()
                    retval, cv2mat= cv2.imencode(".jpeg",output,(cv.CV_IMWRITE_JPEG_QUALITY,cameraQuality)) 
                    jpegData = cv2mat.tostring()     
                    self.wfile.write("--aaboundary\r\n")
                    self.wfile.write("Content-Type: image/jpeg\r\n")
                    self.wfile.write("Content-length: "+str(len(jpegData))+"\r\n\r\n")
                    self.wfile.write(jpegData)
                    self.wfile.write("\r\n\r\n\r\n")
                    time.sleep(0.05)
                return
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        global rootnode, cameraQuality
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)

            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            value=int(upfilecontent[0])
            cameraQuality=max(2, min(99, value))
            self.wfile.write("<HTML> POST OK. Camera Set to <BR><BR>")
            self.wfile.write(str(cameraQuality))

        except:
            pass





