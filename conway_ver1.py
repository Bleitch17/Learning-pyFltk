from fltk import *

def click(wid):
	wid.color(FL_YELLOW)
	wid.deathstate = True
			
def checkstate(wid,L):
		
		for order in range(len(L)):
			
			livecount = 0
				
			if L[order].color() != FL_BLACK:
				
				if L[order - int(len(L)**0.5) - 1].color() == FL_YELLOW:
					livecount += 1
						
				if L[order - int(len(L)**0.5)].color() == FL_YELLOW:
					livecount += 1
						
				if L[order - int(len(L)**0.5) + 1].color() == FL_YELLOW:
					livecount += 1
						
				if L[order - 1].color() == FL_YELLOW:
					livecount += 1
						
				if L[order + 1].color() == FL_YELLOW:
					livecount += 1
						
				if L[order + int(len(L)**0.5) - 1].color() == FL_YELLOW:
					livecount += 1
						
				if L[order + int(len(L)**0.5)].color() == FL_YELLOW:
					livecount += 1
						
				if L[order + int(len(L)**0.5) + 1].color() == FL_YELLOW:
					livecount += 1

			if livecount < 2:
				L[order].deathstate = False
			if livecount == 3:
				L[order].deathstate = True
			if livecount >= 4:
				L[order].deathstate = False
		
		for cell in L:
			if cell.color() != FL_BLACK:
				if cell.deathstate == True:
					cell.color(FL_YELLOW)
					cell.redraw()
				else:
					cell.color(FL_BACKGROUND_COLOR)
					cell.redraw()
						
		for wait in xrange(100000):
			pass	

		Fl.check()

def loopstate(wid,L):
	global gamestate
	gamestate = True
	while gamestate == True:
		frame.do_callback()

def games(wid):
	global gamestate
	if gamestate == True:
		gamestate = False

def clearslate(wid,L):
	for cell in L:
		if cell.color() != FL_BLACK:
			cell.deathstate = False
			cell.color(FL_BACKGROUND_COLOR)
			cell.redraw()
		
w = Fl_Window(800,900)

L = []

gamestate = False

w.begin()
for x in range(80):
	for y in range(80):
		L.append(Fl_Button(x*10,y*10,10,10))

		if y == 0:
			L[-1].hide()
			L[-1].deactivate()
			L[-1].color(FL_BLACK)
		if y == 79:
			L[-1].hide()
			L[-1].deactivate()
			L[-1].color(FL_BLACK)
		if x == 0:
			L[-1].hide()
			L[-1].deactivate()
			L[-1].color(FL_BLACK)			
		if x == 79:
			L[-1].hide()
			L[-1].deactivate()
			L[-1].color(FL_BLACK)
		
		L[-1].deathstate = False
		L[-1].callback(click)	

frame = Fl_Button(250,800,100,100,'next frame')
frame.callback(checkstate,L)

start = Fl_Button(150,800,100,100,'start')
start.callback(loopstate,L)

stop = Fl_Button(350,800,100,100,'stop')
stop.callback(games)

clear = Fl_Button(450,800,100,100,'clear')
clear.callback(clearslate,L)

pause = Fl_Button

w.end()


w.show()
Fl.run()
