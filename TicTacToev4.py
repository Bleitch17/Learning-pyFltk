import socket, sys
from fltk import *

class Game(Fl_Window):
	
	ButtonList = []
	
	X_image = Fl_PNG_Image('X.png')
	X_image = X_image.copy(100,100)
	
	O_image = Fl_PNG_Image('O.png')
	O_image = O_image.copy(100,100)

	def __init__(self, x, y, w, h, label):
		Fl_Window.__init__(self, x, y, w, h, label)
		
		self.begin()
		for x in range(3):
			for y in range(3):
				Game.ButtonList.append(Fl_Button(x*100,y*100,100,100))
				Game.ButtonList[-1].callback(self.click)
		self.end()		
		
		self.host = sys.argv[3]
		self.port = int(sys.argv[1])
		
		self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		
		if sys.argv[2] == 'Server':
			self.s.bind((self.host, self.port)) #If server, bind.
		self.bufsize = 1024
		
		if sys.argv[2] == 'Server':
			self.side = 'X'
		elif sys.argv[2] == 'Client':
			self.side = 'O'
		else:
			print 'Invalid!'
		
		self.O_turn = True	
#======================================================================
		self.fd = self.s.fileno()
		Fl.add_fd(self.fd, self.recieve_data)
#======================================================================
	
	def click(self, wid):
		self.int = str(Game.ButtonList.index(wid))
		
		if self.O_turn == True:
			print 'Os turn'
		elif self.O_turn == False:
			print 'Xs turn'
		
		
		if self.side == 'O' and self.O_turn == True:
			wid.image(Game.O_image)
			wid.deactivate()
			wid.color(FL_WHITE) 
			self.check_win_O()
			
			self.s.sendto(self.int, (self.host, self.port))
			self.O_turn = False
				
		elif self.side == 'X' and self.O_turn == False:
			wid.image(Game.X_image)
			wid.deactivate()
			wid.color(FL_BLACK)
			self.check_win_X()
				
			self.s.sendto(self.int, self.addr)
			self.O_turn = True
			
		else:
			pass
				
	
	def recieve_data(self, fd):
		(self.z, self.addr) = self.s.recvfrom(self.bufsize)
		if self.side == 'O':
			self.O_turn = True
			Game.ButtonList[int(self.z)].image(Game.X_image)
			Game.ButtonList[int(self.z)].deactivate()
			Game.ButtonList[int(self.z)].color(FL_BLACK) 
				
			self.check_win_X()
			
		elif self.side == 'X': #if you are the server
			self.O_turn = False
			Game.ButtonList[int(self.z)].image(Game.O_image)
			Game.ButtonList[int(self.z)].deactivate()
			Game.ButtonList[int(self.z)].color(FL_WHITE)
		
			self.check_win_O()
	
	
	def check_win_O(self):
		if Game.ButtonList[0].color() == FL_WHITE and Game.ButtonList[3].color() == FL_WHITE and Game.ButtonList[6].color() == FL_WHITE or Game.ButtonList[1].color() == FL_WHITE and Game.ButtonList[4].color() == FL_WHITE and Game.ButtonList[7].color() == FL_WHITE or Game.ButtonList[2].color() == FL_WHITE and Game.ButtonList[5].color() == FL_WHITE and Game.ButtonList[8].color() == FL_WHITE or Game.ButtonList[0].color() == FL_WHITE and Game.ButtonList[1].color() == FL_WHITE and Game.ButtonList[2].color() == FL_WHITE or Game.ButtonList[3].color() == FL_WHITE and Game.ButtonList[4].color() == FL_WHITE and Game.ButtonList[5].color() == FL_WHITE or Game.ButtonList[6].color() == FL_WHITE and Game.ButtonList[7].color() == FL_WHITE and Game.ButtonList[8].color() == FL_WHITE or Game.ButtonList[2].color() == FL_WHITE and Game.ButtonList[4].color() == FL_WHITE and Game.ButtonList[6].color() == FL_WHITE or Game.ButtonList[0].color() == FL_WHITE and Game.ButtonList[4].color() == FL_WHITE and Game.ButtonList[8].color() == FL_WHITE:
			self.winner = 'O'
			self.end_game(self.winner)
			
	def check_win_X(self):
		if Game.ButtonList[0].color() == FL_BLACK and Game.ButtonList[3].color() == FL_BLACK and Game.ButtonList[6].color() == FL_BLACK or Game.ButtonList[1].color() == FL_BLACK and Game.ButtonList[4].color() == FL_BLACK and Game.ButtonList[7].color() == FL_BLACK or Game.ButtonList[2].color() == FL_BLACK and Game.ButtonList[5].color() == FL_BLACK and Game.ButtonList[8].color() == FL_BLACK or Game.ButtonList[0].color() == FL_BLACK and Game.ButtonList[1].color() == FL_BLACK and Game.ButtonList[2].color() == FL_BLACK or Game.ButtonList[3].color() == FL_BLACK and Game.ButtonList[4].color() == FL_BLACK and Game.ButtonList[5].color() == FL_BLACK or Game.ButtonList[6].color() == FL_BLACK and Game.ButtonList[7].color() == FL_BLACK and Game.ButtonList[8].color() == FL_BLACK or Game.ButtonList[2].color() == FL_BLACK and Game.ButtonList[4].color() == FL_BLACK and Game.ButtonList[6].color() == FL_BLACK or Game.ButtonList[0].color() == FL_BLACK and Game.ButtonList[4].color() == FL_BLACK and Game.ButtonList[8].color() == FL_BLACK:
			self.winner = 'X'
			self.end_game(self.winner)
		
	def end_game(self,winner):
		print self.winner + '\'s won!'
		
		if self.winner == 'O':
			for button in Game.ButtonList:
				button.deactivate()
				if button.color() == FL_WHITE:
					button.color(FL_GREEN)
		else:
			for button in Game.ButtonList:
				button.deactivate()
				if button.color() == FL_BLACK:
					button.color(FL_GREEN)
	
		
if __name__ == '__main__':				
	Window = Game(250,250,300,300,'TicTacToe' + sys.argv[2])
	Window.show()
	Fl.run()


