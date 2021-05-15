from fltk import *
import random

class Game(Fl_Window):
	
	ButtonList = []
	Mine_ind_list = []
	Invalid = []
	
	flag_image = Fl_PNG_Image("Flag.png")
	flag_image = flag_image.copy(50,50)
	mine_image = Fl_PNG_Image("Mine.png")
	mine_image = mine_image.copy(50,50)

	Flagged = 0
	
	first_click = False 
	
	def __init__(self,width,height,label=None):
		Fl_Window.__init__(self,width,height,label)
		
		self.begin()
		
		for x in range(12):
			for y in range(12):
				Game.ButtonList.append(Fl_Button(x*50,y*50,50,50))
				if x == 0 or x == 11 or y == 0 or y == 11:
					Game.ButtonList[-1].hide()
					Game.ButtonList[-1].deactivate()
					Game.ButtonList[-1].color(FL_BLACK)
					Game.Invalid.append(Game.ButtonList.index(Game.ButtonList[-1]))

				Game.ButtonList[-1].callback(self.click)
	
		self.end()
	
	def start(self,Ind):
#===============================Give each square that is not a bomb a label=================================
		Game.Invalid.append(self.Ind) #Make sure that the first button clicked on does not get a mine placed on it
		Game.Mine_ind_list = random.sample(range(len(Game.ButtonList)),10) # Take 10 unique numbers from the list of Button indicies
		self.placebombs() #set the mines
		
		for buttonInd in range(len(Game.ButtonList)):
			self.mine_counter = 0 #number of bombs around each button
	
			if Game.ButtonList[buttonInd].color() != FL_BLACK and buttonInd not in Game.Mine_ind_list: 
#Check all the buttons that are not edge buttons and not mines:
				Around = [buttonInd + 1, buttonInd - 1, buttonInd + 12, buttonInd - 12, buttonInd + 11, buttonInd - 11, buttonInd + 13, buttonInd - 13]
#Make a list of indices around the button being checked
				for Loc in Around:
					if Loc in Game.Mine_ind_list:
						self.mine_counter += 1 # if there is a bomb at that indicy, increase the counter
				
				if self.mine_counter > 0:
					Game.ButtonList[buttonInd].label(str(self.mine_counter)) #label the button with the number of bombs around it

				elif self.mine_counter == 0:
					Game.ButtonList[buttonInd].label(' ') #give the button a label 0 if there are no bombs around it
				
				Game.ButtonList[buttonInd].labeltype(FL_NO_LABEL)
#============================================================================================================				
	
	def placebombs(self):
		
		self.removed = 0
		for ind in Game.Mine_ind_list:
			if ind in Game.Invalid:
				Game.Mine_ind_list.remove(ind) #Remove any invalid indicies from the list of mine indicies
				self.removed += 1 #Keep track of how many times an indicy is removed
			
		while self.removed > 0: #if at least one indicy has been removed:
			self.r = random.randint(0,len(Game.ButtonList) - 1) #take some more random indicies from the master indicy list
			Game.Mine_ind_list.append(self.r) #append them to the mine indicy list
			Game.Mine_ind_list = set(Game.Mine_ind_list) 
			Game.Mine_ind_list = list(Game.Mine_ind_list) #make sure that there are no duplicate indicies
				
			if len(Game.Mine_ind_list) == 10: 
				self.placebombs()# when there are 10 indicies, call the function again to check to make sure they are all valid
				
		else:
			for mineInd in Game.Mine_ind_list: #take off all the labels on the mines
				Game.ButtonList[mineInd].labeltype(FL_NO_LABEL)		
		
	def click(self,wid):
		
		self.Ind = Game.ButtonList.index(wid) #Find the indicy of the button clicked on
		print(self.Ind)
		
		if Game.first_click == False: #If this is the first click of the game, trigger the start function
			self.start(self.Ind)#send it the indicy of the first button clicked on
			Game.first_click = True #Make sure that this does not happen again
		
		if Fl.event_button() == FL_RIGHT_MOUSE: #if a button is right clicked:
			#if wid.labeltype() == FL_NORMAL_LABEL and wid.color() == FL_GREEN:
			if wid.color() == FL_GREEN:
				wid.image(None)
				wid.color(FL_BACKGROUND_COLOR)
				wid.labeltype(FL_NO_LABEL)
				Game.Flagged -= 1
				#print Game.Flagged, 'Unflagged'
			
			elif wid.labeltype() == FL_NORMAL_LABEL and wid.color() != FL_GREEN:
				pass	
			else:
				wid.labeltype(FL_NORMAL_LABEL)
				wid.image(Game.flag_image)
				wid.color(FL_GREEN)
				Game.Flagged += 1
				#print Game.Flagged,'Flagged' 
				
			if Game.Flagged == len(Game.Mine_ind_list):
				#print 'Initiating winning sequence.'
				for Ind in Game.Mine_ind_list:
					if Game.ButtonList[Ind].color() == FL_GREEN:
						Game.Flagged -= 1
						if Game.Flagged == 0:
							
							for Button in Game.ButtonList:
								Button.labeltype(FL_NORMAL_LABEL)
							Fl.add_timeout(2.0,self.end_game)
								
		if Fl.event_button() == FL_LEFT_MOUSE:
			wid.labeltype(FL_NORMAL_LABEL)
			if Game.ButtonList.index(wid) in Game.Mine_ind_list:
				for buttonInd in Game.Mine_ind_list:
					Game.ButtonList[buttonInd].labeltype(FL_NORMAL_LABEL)
					Game.ButtonList[buttonInd].color(FL_RED)
					Game.ButtonList[buttonInd].image(Game.mine_image)
					Game.ButtonList[buttonInd].redraw()
				Fl.add_timeout(2.0,self.end_game)
				
			self.check_reveal(self.Ind)		
	
	def check_reveal(self,Ind):
		
		Around = [Ind+1,Ind-1,Ind+12,Ind-12,Ind+13,Ind-13,Ind-11,Ind+11]
		
		if Game.ButtonList[Ind].label() != ' ':
			Game.ButtonList[Ind].labeltype(FL_NORMAL_LABEL)
			Game.ButtonList[Ind].redraw()
		
		if Game.ButtonList[Ind].label() == ' ':
			Game.ButtonList[Ind].deactivate()
			for Loc in Around:
				if Game.ButtonList[Loc].labeltype() == FL_NO_LABEL:
					Game.ButtonList[Loc].labeltype(FL_NORMAL_LABEL)
					Game.ButtonList[Loc].redraw()
					self.check_reveal(Loc)

	def end_game(self):
		Run.hide()
	
if __name__ == '__main__':

	Run = Game(600,600)
	Run.show()
	Fl.run()
