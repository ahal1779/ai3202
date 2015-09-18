#!/usr/bin/python
import Queue
import math
import sys

#command line file read
def parseFile(fileDescriptor):
    parsed = []
    for line in fileDescriptor:
        parsed.append(line.rstrip('\n').split(' '))
    return parsed
    
 #take only full commands 
if (len(sys.argv) < 3 or len(sys.argv)>5):
        print 'This is not a correct command line'
        sys.exit()
#world number
number = sys.argv[1]
#heuristic kind
he = sys.argv[2]





class Node():
	
	def __init__(this,key,x,y): #initiate a new node with the given key but no others
		this.key=key
		this.locationx=x
		this.locationy=y
		this.h=0
		this.f=0
		this.parent=None
		this.g=0
		
	def getkey(this):
		return this.key
	def getX(this):
		return int(this.locationx)
	def getY(this):
		return int(this.locationy)
	#implement manhattan heuristic	
def hManhattan(x,y,xg,yg):
	dx=abs(x-xg)
	dy=abs(y-yg)
	return int(10*(dx+dy))
#implement diagonal heuristic	
def hDiagonal(x,y,xg,yg):
	dx=abs(x-xg)
	dy=abs(y-yg)
	return int((10*dx+dy+(14-2*10)*min(dx,dy)))
#which world are we in
if(int(number)==1):
	world = open('World1.txt', 'r')
elif(int(number)==2):
	world = open('World2.txt', 'r')
i=0
x=0
y=0
#Construct the world
mylist=[]
for line in world:
	line.replace(" ","")
	while i < len(line) and len(line)>2:
		if(line[i] != " "):
			mylist.append(Node(line[i],x,y))
		x=x+1
		i=i+2
	i=0
	x=0
	y=y+1
#assign starting and ending values
startx=0
starty=7
endx=9
endy=0

#assign values of heuristinc
def findHe(endX,endY,mylist):
	i=0
	while i< len(mylist):
		if(he=='manhattan'):
			mylist[i].h=hManhattan(mylist[i].getX(),mylist[i].getY(),endX,endY)
		elif(he=='diagonal'):
			mylist[i].h=hDiagonal(mylist[i].getX(),mylist[i].getY(),endX,endY)
		i=i+1
#check the avialabiltiy of the node
def avialable(x,y,mylist):
	i=0
	result=0
	while i<len(mylist):
		if((int(mylist[i].getX())==x+1 and int(mylist[i].getY())==y) or
		(int(mylist[i].getX())==x+1 and int(mylist[i].getY())==y-1) or
		(int(mylist[i].getX())==x and int(mylist[i].getY())==y-1)):
			if(int(mylist[i].getkey())==2):
				result=result+1
		i=i+1
	if int(result)==3:
		return False
	else:
		return True
#given a node find all adjacent values to it
def findAdjacent(x,y,mylist):
	i=0
	newlist=[]
	while i<len(mylist):
		if(mylist[i].getX()==x+1 or mylist[i].getX()==x-1 or mylist[i].getX()==x):
			if(mylist[i].getY()==y+1 or mylist[i].getY()==y-1 or mylist[i].getY()==y):
				if(not (mylist[i].getY()==y and mylist[i].getX()==x)):
					
					if(avialable(mylist[i].getX(),mylist[i].getY(),mylist)):
						newlist.append(mylist[i])
		i=i+1
	return newlist

findHe(endx,endy,mylist)


#main search
def AStar(startx,starty,endx,endy,mylist):
	Open=[]
#find the start
	i=0
	while i<len(mylist):
		if(mylist[i].getY()==starty and mylist[i].getX()==startx):
			Open.append(mylist[i])
			break
		i=i+1
#create closed list
	Closed=[]
	Open[0].f=int(Open[0].h)
	Open[0].g=0
	
	while len(Open)!=0:
		i=0
		c=0
		#find least f(node)
		while i<len(Open):
			if(Open[i].f<Open[c].f):
				c=i
			i=i+1
		#take that value and work on it
		current=Open.pop(c)
		Closed.append(current)
		#indication that we have found a soltuion, but don't stop search
		if (int(current.getX())==endx and int(current.getY())==endy):
			print "Path Found"
		
		#for every one next to the least f(node) value, please find them and add them if the
		#are available 
		for nex in findAdjacent(current.getX(),current.getY(),mylist):
			if(int(nex.getkey())==1 or int(nex.getkey())==0):
				if((current.getX()+1==int(nex.getX()) and current.getY()+1==int(nex.getY())) or 
				(current.getY()+1==int(nex.getY()) and current.getX()-1==int(nex.getX())) or 
				(current.getX()+1==int(nex.getX()) and current.getY()-1==int(nex.getY())) or 
				(current.getY()-1==int(nex.getY()) and current.getX()-1==int(nex.getX()))):
					#assign values for each node
					if(int(nex.getkey())==1):
						value=24
					else:
						value=14
				elif(int(nex.getkey())==1):
					value=20
				else:
					value=10
				nex.g=current.g+value
				f=nex.h+nex.g
				found=0
				found2=0
				#in the closed set
				i=0
				while i<len(Closed):
					if(nex.getY()==Closed[i].getY() and nex.getX()==Closed[i].getX()):
						found2=1
						break
					i=i+1
				#in the open set
				i=0
				while i<len(Open):
					if(nex.getY()==Open[i].getY() and nex.getX()==Open[i].getX()):
						found=1
						break
					i=i+1
				#if it is closed then don't do anything
				#if it is in open, then check if it needs update
				#if it is not in open, add it to open and continue with search
				
				if found2==0:
					if found==1:
						if(f<int(nex.f)):
							nex.f=f
							nex.g=value+current.g
							nex.parent=current
					else:
						nex.f=f
						nex.parent=current
						nex.g=value+current.g
						Open.append(nex)
						
					
	return Closed
#start the search
closed=AStar(startx,starty,endx,endy,mylist)	

#find the end, se we can find the path to it 
i=0
while i<len(mylist):
	if(mylist[i].getY()==endy and mylist[i].getX()==endx):
		current1=mylist[i]
		break
	i=i+1
current_cost=0
#print the values of the nodes that are in path 
print("The number of squares travled to is {} ").format(len(closed))
print("Path is ")
print(" ({},{})").format(current1.getX(),current1.getY())
older=current1
total=0
while not (int(current1.getX())==startx and int(current1.getY())==starty) :
	
	current1=current1.parent
	if((int(current1.getX())+1==int(older.getX()) and int(current1.getY())!=int(older.getY()))or (int(current1.getY())+1==int(older.getY()) and int(current1.getX())!=int(older.getX())) or (int(current1.getX())-1==int(older.getX()) and int(current1.getY())!=int(older.getY()))or (int(current1.getY())-1==int(older.getY()) and int(current1.getX())!=int(older.getX()))):
		if(int(current1.getkey())==1):
			total=total+24
		else:
			total=total+14
	elif(int(current1.getkey())==1):
		total=total+20
	else:
		total=total+10
	print(" ({},{})").format(current1.getX(),current1.getY())
	older=current1
	
print("Cost of this path is: {}").format(total)

	
			
		
		
	

		
	

	
	

