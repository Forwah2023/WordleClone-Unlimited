import sys
from collections import Counter

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
qtw.QApplication.setAttribute(qtc.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
qtw.QApplication.setAttribute(qtc.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

SCREEN_WIDTH =300
SCREEN_HEIGHT =400

class MainWindow(qtw.QWidget):
	def __init__(self,word):
		"""MainWindow constructor"""
		super().__init__()
		self.resize(qtc.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))
		self.setWindowTitle('Wordle Clone')
		layout=qtw.QVBoxLayout()
		self.setLayout(layout)
		grid_layout= qtw.QGridLayout()
		layout.addLayout(grid_layout)
		#dictionary of letter counts in word
		self.count_ltr=Counter(word)
		self.count=0
		self.currRow=0
		self.word=word
		self.currWord=''
		#number of trials =6
		for row in range(6):
			for i in range(len(self.word)):
				Lettrlabel=qtw.QLabel('',self)
				setattr(self,'tile'+str(row)+str(i),Lettrlabel)
				Lettrlabel.setStyleSheet('border:1px solid silver;font-weight: bold;background-color:white;font-size: 13pt;')
				Lettrlabel.setAlignment(qtc.Qt.AlignCenter)
				Lettrlabel.setFixedSize(70,70)
				grid_layout.addWidget(Lettrlabel,row,i)
		self.reset=qtw.QPushButton('Reset',self)
		self.reset.setFixedSize(50,50)
		self.validate=qtw.QPushButton('Verify',self)
		self.validate.setFixedSize(50,50)
		self.gueslength=len(self.word)
		self.guess=qtw.QLineEdit('',self,placeholderText=str(self.gueslength)+'-word guess',maxLength=self.gueslength)
		self.guess.setFixedSize(100,50)
		self.success=qtw.QLabel('Score:'+str(self.count),self)
		self.success.setFixedSize(50,50)
		self.sett=qtw.QPushButton(self)
		self.sett.setFixedSize(25,25)
		icon=qtg.QIcon()
		px=qtg.QPixmap('Icons/gear.png')
		icon.addPixmap(px)
		self.sett.setIcon(qtg.QIcon(icon))
		Hlayout=qtw.QHBoxLayout()
		layout.addLayout(Hlayout)
		Hlayout.addWidget(self.reset)
		Hlayout.addWidget(self.validate)
		Hlayout.addWidget(self.guess)
		Hlayout.addWidget(self.success)
		Hlayout.addWidget(self.sett)
		###signals
		self.guess.textChanged.connect(self.update_tile)
		self.validate.clicked.connect(self.checkWord)
		self.reset.clicked.connect(self.clearAll)
		self.show()
	def update_tile(self,currWord):
		self.currWord=currWord.upper()
		for indx,lettr in enumerate(currWord):
			tile=getattr(self,'tile'+str(self.currRow)+str(indx))
			tile.setText(lettr.upper())
		self.clear_tile(len(self.currWord),len(self.word))
	def clear_tile(self,indx1,indx2):
			for i in range(indx1,indx2):
				pos=len(self.word)
				tile=getattr(self,'tile'+str(self.currRow)+str(i))
				tile.clear()
			
	def checkWord(self):
		if len(self.currWord)<len(self.word):
			return
		if list(self.currWord)==self.word:
			self.updateCount()
			return 
		for indx,lettr in enumerate(self.currWord):
			if self.currWord[indx]==self.word[indx]:
				self.count_ltr[self.currWord[indx]]-=1
				getattr(self,'tile'+str(self.currRow)+str(indx)).setStyleSheet('border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:green; color: white;')
			elif self.currWord[indx] in self.word:
				self.count_ltr[self.currWord[indx]]-=1
				getattr(self,'tile'+str(self.currRow)+str(indx)).setStyleSheet('border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:#DBD050; color:white;')	
			else:
				getattr(self,'tile'+str(self.currRow)+str(indx)).setStyleSheet('border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:#787878; color: white;')
		self.currRow+=1
		self.count_ltr=Counter(self.word)
	def clearAll(self):
		for row in range(5):
			for col in range(len(self.word)):
				tile=getattr(self,'tile'+str(row)+str(col))
				tile.clear()
				tile.setStyleSheet('border:1px solid silver;font-weight: bold;background-color:white;font-size: 13pt;')
	def updateCount(self):
		for i in range(len(self.word)):
			tile=getattr(self,'tile'+str(self.currRow)+str(i))
			tile.setStyleSheet('border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:green; color: white;')
		self.count+=1
		self.currRow=0
		self.success.setText('Score:'+str(self.count))
		qtc.QTimer.singleShot(3000,self.clearAll)
		

if __name__ == '__main__':
	app = qtw.QApplication(sys.argv)
	#set for 5-letter word
	word=['H','E','L','L','O']
	mw = MainWindow(word)
	sys.exit(app.exec())