import sys
import random

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
qtw.QApplication.setAttribute(qtc.Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
qtw.QApplication.setAttribute(qtc.Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons

from keyboard import*

SCREEN_WIDTH =300
SCREEN_HEIGHT =300
TILE_SIZE=40
#Tiles' colors and styles
initStyle='border:1px solid silver;font-weight: bold;margin:0px;background-color:white;font-size: 13pt;'
greenStyle='border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:green; color: white;'
yellowStyle='border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:#DBD050; color:white;'
grayStyle='border:1px solid silver;font-weight: bold;font-size: 13pt;background-color:#787878; color: white;'
class MainWidget(qtw.QWidget):
	def __init__(self,word,wordsFive):
		"""MainWindow constructor"""
		super().__init__()
		self.resize(qtc.QSize(SCREEN_WIDTH, SCREEN_HEIGHT))
		self.setWindowIcon(qtg.QIcon('Icons/WIcon.png'))
		self.setWindowTitle('Wordle Clone')
		layout=qtw.QVBoxLayout()
		self.setLayout(layout)
		grid_layout= qtw.QGridLayout()
		grid_layout.setSpacing(4);
		layout.addLayout(grid_layout)
		self.count=0
		self.maxRow=6
		self.currRow=0
		self.word=word
		# holds list of letters that are not in word 
		self.not_In_Word=[]
		#define global five-word list for reference
		self.wordsFive=wordsFive 
		self.currWord=''
		#number of trials =6
		for row in range(self.maxRow):
			for i in range(len(self.word)):
				Lettrlabel=qtw.QLabel('',self)
				setattr(self,'tile'+str(row)+str(i),Lettrlabel)
				Lettrlabel.setStyleSheet(initStyle)
				Lettrlabel.setAlignment(qtc.Qt.AlignCenter)
				Lettrlabel.setFixedSize(TILE_SIZE,TILE_SIZE)
				grid_layout.addWidget(Lettrlabel,row,i)
		#create buttons and score lables
		self.reset=qtw.QPushButton('Reset',self)
		self.reset.setFixedSize(50,50)
		self.validate=qtw.QPushButton('Verify',self)
		self.validate.setFixedSize(50,50)
		self.gueslength=len(self.word)
		self.guess=qtw.QLineEdit('',self,placeholderText=str(self.gueslength)+'-word guess',maxLength=self.gueslength)
		self.guess.setFixedSize(75,50)
		self.success=qtw.QLCDNumber(self)
		self.success.setSegmentStyle(qtw.QLCDNumber.Flat)
		self.success.setFixedSize(50,50)
		self.keybtn=qtw.QPushButton(self,checkable=True,checked=False)
		self.keybtn.setFixedSize(50,50)
		settingIcon=qtg.QIcon()
		px=qtg.QPixmap('Icons/keyboard-full.png')
		settingIcon.addPixmap(px)
		self.keybtn.setIcon(qtg.QIcon(settingIcon))
		# horizontal button layout
		Hlayout=qtw.QHBoxLayout()
		layout.addLayout(Hlayout)
		Hlayout.addWidget(self.reset)
		Hlayout.addWidget(self.validate)
		Hlayout.addWidget(self.guess)
		Hlayout.addWidget(self.success)
		Hlayout.addWidget(self.keybtn)
		
		WarnLabel=qtw.QLabel('Welcome!',self)
		WarnLabel.setStyleSheet('font-size: 12pt; font-weight:bold;')
		WarnLabel.setAlignment(qtc.Qt.AlignCenter)
		self.WarnLabel=WarnLabel
		layout.addWidget(WarnLabel)
		qtc.QTimer.singleShot(5000,self.clearWarningT)
		###signals
		self.guess.textChanged.connect(self.update_tile)
		self.validate.clicked.connect(self.checkWord)
		self.reset.clicked.connect(self.clearAll)
		self.keybtn.clicked.connect(self.show_keyboard)
		self.show()
	def update_tile(self,currWord):
		# do nothing if last row is reached
		if self.currRow==self.maxRow:
			return
		self.currWord=currWord.upper()
		for indx,lettr in enumerate(currWord):
			tile=getattr(self,'tile'+str(self.currRow)+str(indx))
			tile.setText(lettr.upper())
		self.clearUnusedTiles(len(self.currWord),len(self.word))
	def clearUnusedTiles(self,indx1,indx2):
			for i in range(indx1,indx2):
				pos=len(self.word)
				tile=getattr(self,'tile'+str(self.currRow)+str(i))
				tile.clear()
			
	def checkWord(self):
		if len(self.currWord)<len(self.word):
			return
		if self.currWord.upper() not in self.wordsFive:
			self.WarnLabel.setText('Not in word list!')
			qtc.QTimer.singleShot(3000,self.clearWarningT)
			return
		if list(self.currWord)==self.word:
			self.updateCount()
			return 
		for indx,lettr in enumerate(self.currWord):
			if self.currWord[indx]==self.word[indx]:
				self.setTileColor(self.currRow,indx,greenStyle)
			elif self.currWord[indx] in self.word:
				self.setTileColor(self.currRow,indx,yellowStyle)	
			else:
				self.setTileColor(self.currRow,indx,grayStyle)
				self.not_In_Word.append(lettr.upper())
				if hasattr(self,'kbd'):
					kbdTile=getattr(self.kbd.ui,'label'+lettr.upper())
					kbdTile.setStyleSheet(grayStyle)				
		self.currRow+=1
		if self.currRow==self.maxRow:
			self.WarnLabel.setText('Current word was: {}'.format(''.join(self.word)))
			self.clear_Kbd()
			qtc.QTimer.singleShot(3000,self.clearAll)
			
		self.guess.clear()
	def setTileColor(self,row,col,style):
		getattr(self,'tile'+str(row)+str(col)).setStyleSheet(style)
	def clearAll(self):
		for row in range(self.maxRow):
			self.clearRow(row)
		self.currRow=0
		self.currWord=''
		self.WarnLabel.setText('New challenge!')
		qtc.QTimer.singleShot(2000,self.clearWarningT)
		if self.wordsFive !=[]:
			self.word=list(random.choice(self.wordsFive))
		else:
			self.WarnLabel.setText('No new word found!')
			qtc.QTimer.singleShot(3000,self.clearWarningT)
	def clearRow(self,row):
		for col in range(len(self.word)):
			tile=getattr(self,'tile'+str(row)+str(col))
			tile.clear()
			tile.setStyleSheet(initStyle)
	def clear_Kbd(self):
		if hasattr(self,'kbd'):
			if self.not_In_Word==[]:
				return
			for lettr in self.not_In_Word:
				kbdTile=getattr(self.kbd.ui,'label'+lettr.upper())
				kbdTile.setStyleSheet(initStyle)
	def clearWarningT(self):
		self.WarnLabel.setText('')
	def updateCount(self):
		for i in range(len(self.word)):
			tile=getattr(self,'tile'+str(self.currRow)+str(i))
			tile.setStyleSheet(greenStyle)
		self.count+=1
		self.success.display(self.count)
		self.clear_Kbd()
		qtc.QTimer.singleShot(3000,self.clearAll)
	def show_keyboard(self):
		if hasattr(self,'kbd'):
			if not self.keybtn.isChecked():
				self.kbd.hide()
			else:
				self.kbd.show()
		else:
			self.kbd=KbdWindow()
			self.kbd.show() # may be suppressed
			
class KbdWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()
		self.ui=Ui_Keyboard()
		self.ui.setupUi(self)
		self.setWindowIcon(qtg.QIcon('Icons/WIcon.png'))
		self.setWindowTitle('Wordle Clone')
		self.show()
		
class MainWindow(qtw.QMainWindow):
	def __init__(self,mainwidget):
		super().__init__()
		self.setCentralWidget(mainwidget)
		self.setWindowIcon(qtg.QIcon('Icons/WIcon.png'))
		self.setWindowTitle('Wordle Clone')
		#menu bar
		menubar=self.menuBar()
		help_menu=menubar.addMenu('Help')
		about_action=help_menu.addAction('About',self.show_about)
		doc_action=help_menu.addAction('How to play',self.show_doc)
		self.show()
	def show_about(self):
		qtw.QMessageBox.about(self,"Wordle Clone PyQt5","This is a clone of the globally famous game: Wordle.\nCopyright (C) 2023 Forwah Amstrong, Ph.D \n<lmsoftware2023@gmail.com> \nGNU General Public Licence \nFugue Icons (C) 2013 Yusuke Kamiyamane.")
		
	def show_doc(self):
		qtw.QMessageBox.information(self,"How to play.","1. Each guess must be a valid 5-letter word.\n 2. The color of the tiles will change to show how close\n your guess was to the word.\n 3. Green implies the letter is in the word and in the correct spot.\n 4. Yellow means the letter is in the word but in the wrong spot.\n 5. Gray means letter is not in the word in any spot.  ")
	def closeEvent(self,Event):
		'''Overrides the default close function for QMainWindow'''
		#closes main window along with subwindows 
		if hasattr(self.centralWidget(),'kbd'):
			self.centralWidget().kbd.close()
		super().closeEvent(Event)
def main():
	global wordsFive
	app = qtw.QApplication(sys.argv)
	try: 
		with open('data/FivesWords.txt','r') as f:
			Wlist=f.read().splitlines()
			#set for 5-letter word
			wordsFive=[W.upper() for W in Wlist if len(W)==5]
			print('There are {} in this list'.format(len(wordsFive)))
			#initilize first word of the day
			word=list(random.choice(wordsFive))
			#print('current word is {}'.format(word))
			
	except FileNotFoundError:
		print('Empty word list. Please check data!')
		word=['']*5	
		wordsFive=[]
		
	mw = MainWidget(word,wordsFive)
	QM=MainWindow(mw)####
	sys.exit(app.exec())
if __name__ == '__main__':
	main()
