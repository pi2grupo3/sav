import cv2.cv as cv
import cv2
import sys

class Boot:

	def __init__(self, confFile="conf.txt"):
		self.data = self.openConfFile(confFile)
		print self.data

	def disclamer(self):
		print "\nAutor: Eusyar Alves" + "\n\nO conteudo desse codigo foi feito com base nos exemplos encontrados no pacote oficial da biblioteca opencv, bem como no capitulo" 
		print "final do livro : OpenCV 2 Computer Vision Application Programming Cookbook. A implementacao dos algoritimos de deteccao de pedestre sao chamadas feitas a " 
		print "biblioteca OpenCV, sendo apenas de autoria do aluno a logica de separacao de imagens. " + "\n\n20/05/2013\n\n"
		
	def howToUse(self):
		print "\n\n"	
		
	def openConfFile(self, confFile):
		dataFile = open(confFile)
		dataDic = {}
		for item in dataFile.readlines():
			if(item.startswith("#") or item.startswith("\n")):
				continue
			key, value = item.rstrip().split('=')
			dataDic[key] = value
		dataFile.close()		
		return dataDic
		
	def getProperty(self, key):
		return self.data[key]

	def freeCamera(self, cameraObject):
		del(cameraObject)
