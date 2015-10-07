#!/usr/bin/python
import math
import sys

myGraph=[]#this is where all nodes of the graph are
MaxIteration=1000# don't exceed this when looking for convergens
gamma=0.5
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
worldName = sys.argv[1]
#epsilon values: note I named gamma epsilon for the rest of the code
gamma= float(sys.argv[2])
class Node():
	def __init__(this,key,x,y,R): #initiate a new node with the given key but no others
		this.key=key
		this.locationx=x
		this.locationy=y
		this.location=[x,y]
		this.R=R#Reward
		this.U=R#initiate with reward
		this.US=R#initiate with reward
		this.action=None
		#initiate goal and wall
		if(key==2):
			this.action='wall '
		if(key==50):
			this.action='Goal'
		this.parent=None
		
	def getLocation(this):
		return this.location
	def getY(this):
		return int(this.locationy)
	def getX(this):
		return int(this.locationx)
	def getY(this):
		return int(this.locationy)
		
#get the file values
def openFileMatrix(matrix):
	m = []
	for line in matrix:
		m.append(line[0:-1].split(" "))
	return m[0:-1]
#open the file and convert it to matrix
world = open(worldName, 'r')
r=openFileMatrix(world)
#create a graph of nodes
def create_graph(world):
	i=0
	k=0
	while i<len(world[0]):
		k=0
		while k<8:
			#for each, assign the reward depending on the key value
			if(int(world[k][i])==0):
				myGraph.append(Node(0,i,k,0))
			elif(int(world[k][i])==1):
				myGraph.append(Node(1,i,k,-1))
			elif(int(world[k][i])==2):
				myGraph.append(Node(2,i,k,0))#special case of wall, can't go through
			elif(int(world[k][i])==3):
				myGraph.append(Node(3,i,k,-2))
			elif(int(world[k][i])==4):
				myGraph.append(Node(4,i,k,1))
			elif(int(world[k][i])==50):
				myGraph.append(Node(50,i,k,50))
			k=k+1
		i=i+1
			
create_graph(r)	

#search in graph to find if this square exists
#return true if found and false otherwise
def exists(location):
	for i in myGraph:
		if(int(location[0])==int(i.locationx) and int(location[1])==int(i.locationy)):
			return True
	
	return False
	
# just like exists, but returns the node itself
def find(location):
	for i in myGraph:
		if(int(location[0])==int(i.locationx) and int(location[1])==int(i.locationy)):
			return i
#compute the maximum choice of utility of the surrouding squares
#determines the action that we will be taking
#if going left or right, we check up and down to get the utility of them
#if going up or down, we check right and left to get their utility and compute the %20 misschanses
def adjacent(location,epsilon):
	myadjacent=[]
	myactions=[]
	locations=[]
	#check for the left node
	if(exists([int(location[0])-1,int(location[1])]) ):
		#Left
		# find the up and down nodes
		values=getUD(location)
		# add the %80 output outcome
		u=(float(find([int(location[0])-1,location[1]]).U))*0.8
		# for up and down, calculate their utility and mutilyt by %10 for each
		for i in values:
			u=u+(float(i.U))*0.1
		# add the value to be compared
		myadjacent.append(u)
		# add the action that will be associated with the maximum
		myactions.append("left")
	#rest are excactly the same
	if(exists([int(location[0])+1,int(location[1])]) ):
		#Right
		values=getUD(location)
		u=(float(find([int(location[0])+1,location[1]]).U))*0.8
		for i in values:
			u=u+(float(i.U))*0.1
		myadjacent.append(u)
		myactions.append("right")
	if(exists([int(location[0]),int(location[1])-1]) ):
		#Down
		values=getRL(location)
		u=(float(find([int(location[0]),int(location[1])-1]).U))*0.8
		for i in values:
			u=u+(float(i.U))*0.1
		myadjacent.append(u)
		myactions.append("up")
	if(exists([int(location[0]),int(location[1])+1])):
		#UP
		values=getRL(location)
		u=(float(find([int(location[0]),int(location[1])+1]).U))*0.8
		for i in values:
			u=u+(float(i.U))*0.1
		myadjacent.append(u)
		myactions.append("down")
	# determine the value 
	index=myadjacent.index(max(myadjacent))
	find(location).action=myactions[index]
	return max(myadjacent)
#return a list of the availabe up and down squres of a givien location
def getUD(location):
	myadjacent=[]
	if(exists([int(location[0]),int(location[1])-1]) ):
		myadjacent.append(find([location[0],int(location[1])-1]))
	if(exists([int(location[0]),int(location[1])+1]) ):
		myadjacent.append(find([location[0],int(location[1])+1]))
	return myadjacent
#return a list of the availabe right and left squres of a givien location
def getRL(location):
	myadjacent=[]
	if(exists([int(location[0])-1,int(location[1])]) ):
		myadjacent.append(find([int(location[0])-1,location[1]]))
	if(exists([int(location[0])+1,int(location[1])]) ):
		myadjacent.append(find([int(location[0])+1,location[1]]))
	return myadjacent
	
#main calculation of mdp
def value_iteration(world,epsilon):
	#define a new utility function
	i=0
	delta=0
	#make sure we have a common ground before starting
	for current in myGraph:
			current.US=current.U
		#trying to avoid infiite looping
	while i<MaxIteration:
		delta=0
		#for all nodes, except goals and walls, calcuate output
		for current in myGraph:
			if(int(current.key)!=50 and int(current.key)!=2):
				#using the formula and adjacent returns the maximum
				current.US=(int(current.R)+epsilon*adjacent(current.location,epsilon))
				delta=max(delta,abs(float(current.U)-float(current.US)))
		
		if(delta<float(gamma*(1-epsilon)/epsilon)):
			print("Solution Found")
			return 0
		#change the values for the next round	
		for current in myGraph:
			current.U=current.US
		i=i+1;
		

path=[]
values=[]
#move from start to end and print 
# the values and locations
#until we get to end
def findTrace(start,end):
	
	start
	while start!=end:
		path.append(start)
		path.append(find(start).US)
		path.append(find(start).action)
		print("Square:{}, Action:{}, Utility:{}").format(start,find(start).action,find(start).US)
		if(find([int(start[0]),int(start[1])]).action=="up"):
			if(exists([int(start[0]),int(start[1])-1])):
				start=find([int(start[0]),int(start[1])-1]).location
		elif(find([int(start[0]),int(start[1])]).action=="down"):
			start=find([int(start[0]),int(start[1])+1]).location
		elif(find([int(start[0]),int(start[1])]).action=="right"):
			start=find([int(start[0])+1,int(start[1])]).location	
		elif(find([int(start[0]),int(start[1])]).action=="left"):
			start=find([int(start[0])-1,int(start[1])]).location
	print("Square:{}, Action:{}, Utility:{}").format(start,find(start).action,find(start).US)

# for all values print the whole grid
#
def printGrid(world):
	action=[]
	# make them all the same length, for a good formating
	for current in myGraph:
		if(current.action=="up"):
			current.action="up   "
		elif(current.action=="down"):
			current.action="down "
		elif(current.action=="left"):
			current.action="left "
		
		action.append(current.action)
	#print every row,
	# it is dones this way, due to the fact that our
	#list has the nodes in a vertical order,
	
	i=0
	while i<8:
		sys.stdout.write(action[i]+"  "+ action[i+8]+"  "+action[i+16]+"  "+ action[i+24]+"  "+action[i+32]+"  "+ action[i+40]+"  "+action[i+48]+"  "+ action[i+56]+"  "+action[i+64]+"  "+action[i+72]+"  ")
		print("")
		i=i+1
			
#runing the code
value_iteration(r,0.9)
findTrace([0,7],[9,0])
printGrid(r)




