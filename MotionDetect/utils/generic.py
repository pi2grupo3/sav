import cv2.cv as cv
import cv2
import sys
import os,logging
import time

from time import time
from datetime import datetime

'''
Autor: Eusyar Alves de Carvalho

Doc: A classe ut indica utilidades, um forma simples de incapsular chamadas a modulos mais
 complexos, no caso o cv e o cv2, bem como oferecer utilidades genericas.

'''
class ut:

    '''
    Cria uma imagem. 
    FIXME: Retorna um numpy ou um cvmat ou uma iplimage
    '''
    @staticmethod
    def img(imgSize, depth = cv.IPL_DEPTH_8U, channels = 3):
        return cv.CreateImage( cv.GetSize( imgSize ), depth, channels )

    @staticmethod
    def query(cam_rec):
        return cam_rec.read()	
		
    @staticmethod	
    def storage(self): 
        return cv.CreateMemStorage(0)	
			
    @staticmethod
    def drawRect(rects, dest, color):	
        (tlx, tly, brx, bry) = rects
        cv2.rectangle(dest, (int(tlx),int(tly)) , (int(brx),int(bry)), color)
	
    @staticmethod
    def insindeOnePoint(rect, rect2):
        (rx, ry, rw, rh) = rect
        (qx, qy, qw, qh) = rect2
        return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

    @staticmethod
    def area(rect):
        rx1, ry1,rx2, ry2  = rect
        if(rx1 > rx2):
            rw = rx1 - rx2
        else :
            rw = rx2 - rx1			
        if(ry1 > ry2):
            rh = ry1 - ry2
        else :
            rh = ry2 - ry1			
        return rh*rw

    @staticmethod
    def insindeTwoPoint(rect, rect2, offset):
        rx1, ry1,rx2, ry2  = rect
        qx1, qy1,qx2, qy2  = rect2		
		
        ra = ut.area(rect)
        qa = ut.area(rect2)
		
        # Qa pode estar dentro de ra
        if(ra > qa):
            return (rx1 - offset <= qx1) and (ry1 - offset <= qy1) and (rx2 + offset >= qx2) and (ry2 + offset >= qy2)
        else:
            return (qx1 - offset <= rx1) and (qy1 - offset <= ry1) and (qx2 + offset >= rx2) and (qy2 + offset >= ry2)

    @staticmethod
    def pointInsideRect(rect,point):
        x1,y1,x2,y2 = rect
        x3,y3 = point
        return x3 >= x1 and x2 >= x3 and y3 >= y1 and y2 >= y3

    @staticmethod
    def cam(source = -1):		
        if(source is "0"):
            source = 0		
        cam_rec = cv2.VideoCapture(source)
        if cam_rec is None or not cam_rec.isOpened():
            print "ERROR || A camera nao foi aberta"
            sys.exit(1)
        return cam_rec

    @staticmethod
    def writer(source, height, width, dest_name, extension='avi',codec=cv.CV_FOURCC('M','J','P','G')):			    
        fps = 25

        '''
        CV_FOURCC('P','I','M','1') = MPEG-1 codec
        CV_FOURCC('M','J','P','G') = motion-jpeg codec (does not work well)
        CV_FOURCC('M','P','4','2') = MPEG-4.2 codec
        CV_FOURCC('D','I','V','3') = MPEG-4.3 codec
        CV_FOURCC('D','I','V','X') = MPEG-4 codec
        CV_FOURCC('U','2','6','3') = H263 codec
        CV_FOURCC('I','2','6','3') = H263I codec
        CV_FOURCC('F','L','V','1') = FLV1 codec
        '''

        #I420,IYUV,DIB -- avi
        #fourcc = cv.CV_FOURCC('M', 'P', '4', '2')
        #fourcc = cv.CV_FOURCC('F','L','V','1')
        #fourcc = cv.CV_FOURCC('M','J','P','G')
        if(codec == 'mp42'):
            codec = cv.CV_FOURCC('H','2','6','4')
        if(codec == 'flv'):
            codec = cv.CV_FOURCC('P','I','M','1')
        fourcc = codec
        print dest_name+"."+extension
        return cv2.VideoWriter(dest_name+"."+extension, fourcc,fps, (width, height ))
   
    @staticmethod
    def newTime(oldTime):
        nowTime = time()
        diffTime = nowTime - oldTime
        hours,rest = divmod(diffTime,3600)
        minutes, seconds = divmod(rest,60)
        #if(hours >= 1):
        if(seconds > 30):
            return diffTime
        else:
            return False

    @staticmethod
    def timeToFileName():
        strDate = datetime.today().replace(microsecond=0)
        fileName = str(strDate)
        fileName = fileName.replace('-','')
        fileName = fileName.replace(' ','_')
        fileName = fileName.replace(':','-' )
        return fileName

    '''
    Esse metodo foi copiado de samples/python2/commom.py
    '''
    @staticmethod
    def draw_str(dst, (x, y), s):
        cv2.putText(dst, s, (x+1, y+1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness = 2, lineType=cv2.CV_AA)
        cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)

    @staticmethod
    def displayImageInfo(image):
        print '---------------Image INFO---------------'
        print 'Width X Height : ' + str(image.width) + " x " + str(image.height)
        print 'Pixel Depth    : ' + str(image.depth)
        print 'Channles       : ' + str(image.nChannels)
        print '----------------------------------------'

    @staticmethod
    def toGrayScale(imgSrc, imgDst):
        cv.CvtColor(imgSrc, imgDst , cv.CV_RGB2GRAY)
	
    @staticmethod
    def empty(img):
        print img.tostring()
        for x in xrange(img.cols):
            for y in xrange(img.rows):
                if(img[y, x] != 0 ):
                    return False
        return True
	
    @staticmethod
    def running():
        c = cv.WaitKey(20)
        if c == ord('q'):
            return False
        return True
		
class FPS:

    def __init__(self):
        self.fps = 0
        self.fps_counter = 0
        self.old_time = self.clock()
        self.actual_time = self.clock()
        self.start = self.clock()
	
    def clock(self):
        return cv2.getTickCount() / cv2.getTickFrequency()

    def update(self):
        ret = self.fps 
        self.fps_counter += 1;
        self.actual_time = self.clock()
        if( self.old_time + 1 <  self.actual_time ):
            self.old_time = self.actual_time
            self.fps = self.fps_counter
            self.fps_counter = 0
            return self.fps        
        return self.fps
		
    def time(self):
        today = datetime.time(datetime.now())
        return str(today.hour) + ":" +str(today.minute) + ":" + str(today.second)
			
    def timer(self):
        return ((self.clock() - self.start)*1000)
	
'''
Logs - baseado na classe exemplo de http://swaroopch.com/notes/python_pt-br-biblioteca_padrao/
'''
class log:
	
    def __init__(self,logFile="running.log"):
        self.logging_file = os.path.join(os.getenv('HOME'), logFile)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s:%(levelname)s:%(message)s',
            filename = self.logging_file,
            filemode = 'w',
        )
    
    def info(self, msg):
        logging.info(msg)
	
    def debug(self, msg):
        logging.debug(msg)
		
    def warning(self, msg):
        logging.warning(msg)
			
if __name__=="__main__":
    
    newtime = datetime.now()
    time.sleep(4)
    print ut.newTime(newtime)

			
