from fltk import *
import random
import pickle as p

DifList = []
ButtonList = []
sequence = []
play_sequence = []
Pressed_List = []
Pressed_List_Check = []

counter = 0

def game(wid):
	check = 0
	if wid not in ButtonList:
		global counter, Pressed_List_Check, Pressed_List, play_sequence
		counter = 0
		Pressed_List_Check = []
		Pressed_List = []
		play_sequence = []
		
		
		random.shuffle(sequence)
		
		ButtonList[0].color(FL_RED)
		ButtonList[1].color(FL_BLUE)
		ButtonList[2].color(FL_YELLOW)
		ButtonList[3].color(FL_GREEN)
		
		for button in ButtonList:
			button.redraw()

		play_sequence.append(sequence[counter])
		wid.deactivate()
		
		execute()
		
		global counter
		counter += 1
	
	else:
		Pressed_List_Check.append(wid)
		if Pressed_List_Check[check] == Pressed_List[check]:
			check += 1
			if len(Pressed_List_Check) == len(Pressed_List):
				if Pressed_List_Check == Pressed_List:
					if play_sequence == sequence:
						sc0 = len(play_sequence)
						win(sc0)
					else:
						play_sequence.append(sequence[counter])
				
						global Pressed_List_Check, Pressed_List
						Pressed_List_Check = []
						Pressed_List = []
		
						execute()
						
						global counter
						counter += 1
				else:
					sc0 = len(play_sequence) - 1
					lose(sc0)
		else:
			sc0 = len(play_sequence) - 1
			lose(sc0)

def execute():
	for button in ButtonList:
		button.deactivate()
	s = 1
	for button in play_sequence:
		Pressed_List.append(ButtonList[button])
		Fl.add_timeout(s,press,button)
		s += 1
	Fl.add_timeout(s,active)
	
def press(button):
	ButtonList[button].value(1)
	Fl.add_timeout(0.5,release,button)
		
def release(button):
	ButtonList[button].value(0)

def active():
	for button in ButtonList:
		button.activate()

def win(sc0):
	for button in ButtonList:
		button.color(FL_BACKGROUND_COLOR)
		button.redraw()
	
	start.activate()
	print 'You win!'
	set_high_score(sc0)
	
	w.hide()
	dif.show()

def lose(sc0):
	for button in ButtonList:
		button.color(FL_RED)
		button.redraw()
	print 'You lose!'
	set_high_score(sc0)
	Fl.add_timeout(2,restart)

def restart():
	start.activate()
	w.hide()
	dif.show()

def set_Level(wid):
	global sequence
	sequence = [0,1,2,3] * int(wid.label())
	w.show()
	dif.hide()

def set_high_score(sc0):
	sb = HighScores
	sb.sort()
	if len(sb) < 10:
		sb.append([sc0, player_name])
		print 'You made the highscores!'

	if len(sb) >= 10:
		if sc0 > sb[-1]:
			sb.append([sc0, player_name])
			sb.remove(HighScores[1])
			print 'You made the HighScores!'
	
	scores = open('Highscores','w')
	sb.sort()
	sb = sb[::-1]
	p.dump(sb,scores)
	scores.close()

def high_Score(wid):
	try:
		scores = open('Highscores')
		ScoreBoard = p.load(scores)
		place = 1
		for player in range(len(ScoreBoard)):
			print place,':',ScoreBoard[player][0],'Name: ',ScoreBoard[player][1]
			place += 1
	
		scores.close()
	except:
		print 'No scores available.'
		scores.close()
	
			


try:
	sco = open('Highscores')
	HighScores = p.load(sco)
	sco.close()
except:
	HighScores = []



player_name = raw_input('Enter your name: ')

w = Fl_Window(300,400,'Simon Says')
dif = Fl_Window(700,100,'Difficulty Select')

if player_name == 'res3t':
	sb = open('Highscores','r')
	for line in sb:
		line = ''
	HighScores = []
	sb.close()

w.begin()

for x in range(2):
	for y in range(2):
		ButtonList.append(Fl_Button(150*x,150*y,150,150))
		ButtonList[-1].callback(game)

start = Fl_Button(100,300,100,100,'Start')
start.callback(game)

w.end()


dif.begin()

level = 1
for x in range(5):
	DifList.append(Fl_Button(100 * x,0,100,100))
	DifList[-1].label(str(level))
	DifList[-1].callback(set_Level)
	level += 1

h_score = Fl_Button(525,0,150,100,'Show Scoreboard:')
h_score.callback(high_Score)

dif.end()

dif.show()
Fl.run()
