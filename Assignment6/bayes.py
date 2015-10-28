#!/usr/bin/env python
#Ahmed M Alismail
#ahal1779
import getopt, sys


BayesNetwork={}#where to save the nodes of the whole program
evidence={} # store the reasoning for each variable
evidence["No Evidence"]=0
evidence["Predictive"]=1
evidence["Diognostic"]=2
evidence["Sibling"]=3




class BayesNode(object):
	#store values for identifyng each node
	def __init__(this, name, appr):
		this.name = name
		this.appr = appr
		this.probs = {}
		this.parent = {}
		this.child = {}
		this.condProb = None
		this.condProbCalc = False
	#function that will be used to
	#set the relationship between every node and it's neighbors
	def setProb(this, key, value):
		this.probs[key] = value


	def setParent(this, node):
		this.parent[node.name] = node


	def setChild(this, node):
		this.child[node.name] = node

#check whether or not the node exists in the netwokr
def exists(node):
	c=node.upper()
	for n in BayesNetwork.values():
		if (n.appr == c):
			return True
	
	return False
#same as exists yet this will return the actual node
#in the case of exists, only true or false will be returned
def find(node):
	c=node.upper()
	for n in BayesNetwork.values():
		if (n.appr == c):
			return n
	
	return None

#find the marginal values for 
#every probability
#These values are the values that should be
#calculated at the begining

def findConditional(node):
	#check whether it is a leaf or root or in between
	if(len(node.parent)>0):
		#make sure the node exists before 
		#calling any function related to it
		if(exists(node.appr)):
			margin = float(0.0)
			marginParent = {}
		#search for all the values that are affecting this node
		#if you find any, add that to the list
			for parentNode in node.parent.values():
				if (parentNode.condProbCalc == False):
					findConditional(parentNode)
				marginParent[parentNode.appr] = parentNode.condProb
		#make sure we don't add any values that is not
		#a parent of this current value
			for (key, value) in node.probs.items():
				current = 1.0
				n = False
				for c in key:
					if(c.upper()!="X" and c.upper()!="D"):
						if (c == '~'):
							n = True
						else:
							if (n == False):
								current *= marginParent[c]
							else:
								n = False
								current *= (1 - marginParent[c])
				#add these values to the final margin
				margin += value * current

			node.condProb =float(margin)
			node.condProbCalc = True
	#in the case of a parent node
	#this is straight forward
	#just make sure you add that it is initilized
	elif(len(node.parent)==0):
		#double check that the node exist
		if(exists(node.appr)):
			#check the values related to this value
			margin = node.probs.values()
			if (len(margin) != 1):
				print "Not Initilized"
			else:
				#the first value in the probabliites list 
				#correspond to the value of this node
				node.condProb = float(margin[0])
				node.condProbCalc = True
				#update the check relationship
		else:
			#if it doesn't exist no further computations are nedded
			print "This node doesn't exist"
	return 0
def setPrior(a,val):
	#we only update P and S
	if(a.upper()=="P" or a.upper()=="S"):
		for n in BayesNetwork.values():
			if n.appr == a.upper():
				n.setProb(a.upper(),val)
				print "Value set"
				
	else:
		
		print "Cann't be Done"
		print "Must choose either P or S"
		sys.exit(0)
		#make sure to uppdate the values calculated 
		#that might be affected with the current value that has been changed
	for n in BayesNetwork.values():
		n.condProbCalc = False
			
	for n in BayesNetwork.values():
			if n.condProbCalc == False:
				findConditional(n)
				
	
#This calculation is to convert the distribution 
#of probabilites into small probabilites 

def convertDistribution(string, listS):
		x = True
		for c in string:
			if c.isupper():
				b = string.replace(c, c.lower())
				c = string.replace(c, "~"+c.lower())
				if not listS.has_key(b):
					convertDistribution(b, listS)
				if not	listS.has_key(c):
					convertDistribution(c, listS)
				x = False

		if (x):
			listS[string] = True
#consider the relationship between each two  nodes
def reasonOfEvidence(node, dep):
		#if they are the same node, no evidence is needed
		if (node.name == dep.name):
			return evidence["No Evidence"]
			
		#otherwize, check if it is an ancestor or a child 
		#first check the children
		children = []
		children.append(node)
		while (len(children) > 0):
			for current in children:
				if (current.name == dep.name):
					return evidence["Diognostic"]
				children.remove(current)
				for arg in current.child.values():
					children.append(arg)
		#if not found in the children
		#then check the parents list.
		parents = []
		parents.append(node)
		while (len(parents) > 0):
			for current in parents:
				if (current.name == dep.name):
					return evidence["Predictive"]
				parents.remove(current)
				for arg in current.parent.values():
					parents.append(arg)
	#if they are not a parent nor a child
	#the only explanation is that they are on the same
	#lvl as the current node
		return evidence["Sibling"]	
		
def checkIfIndependent(node1, node2):
	return (node1.appr == "P" and node2.appr == "S") \
			or (node1.appr == "S" and node2.appr == "P")
#calculate the conditional value for two given values
#first we must check the the evidence that we have
#and how it relates to the current node
def calcConditional(node,dep,nodeNegative,depNegative):	
	#check the reasoning
		reason = reasonOfEvidence(node, dep)
		#if no evidense is needed then, the value
		#must be 1 since this is the same node
		if (reason == evidence["No Evidence"]):
			return 1
		#if the reasoning is predictive, then we must find the level
		#of the current node with relationship to the 
		#other node and calcuate the values 
		#based on these dependcies
		elif (reason == evidence["Predictive"]): 
			#direct connection
			if (node.probs.has_key(dep.appr)): 
				if nodeNegative == "~":
					return 1-node.probs[depNegative + dep.appr]
				else:
					return node.probs[depNegative + dep.appr]

			#if not direct connection, then we must consider 
			#the path to the desired node
			#the socond case
			else: 
				if not (node.parent.has_key(dep.name)): 
					nodeParent = None
					for parent in node.parent.values():
						nodeParent = parent
					first = calcConditional(node, nodeParent, nodeNegative, "")
					prob= calcConditional(nodeParent, dep, "", depNegative)
					second= calcConditional(node, nodeParent, nodeNegative, "~")
					nprob = 1-prob
					inter1=float(first*prob)
					inter2=float(second*nprop)
					sum1=inter1+inter2

					return sum1

				else: 
					sum2 = None
					for current in node.parent.values():
						if (current.name != dep.name):
							sum2 = (current.appr, current.condProb)
					
					first = ((depNegative+dep.appr+sum2[0], sum2[0]+depNegative+dep.appr), dep.condProb * sum2[1])
					second = ((depNegative+dep.appr+"~"+sum2[0], "~"+sum2[0]+depNegative+dep.appr), dep.condProb * (1-sum2[1]))


					prob1 = first[1] * node.probs.get(first[0][0], node.probs.get(first[0][1], False))
					prob2= second[1] * node.probs.get(second[0][0], node.probs.get(second[0][1], False))

					if nodeNegative == "~":
						return float(1 - ((prob1 + prob2) / dep.condProb))
					else:
						return float((prob1 + prob2) / dep.condProb)
		#In the case of them being sibligs
		#make sure to find if any intercasulaity exists between
		#the two 
		elif (reason == evidence["Sibling"]):
			intercasual = False
			add = None
			for current1 in node.parent.values():
				for current2 in dep.parent.values():
					if current1 == current2:
						add = current1
						intercasual = True
						break
			if (intercasual):
				first = calcConditional(node, add, nodeNegative, "")
				prob1 = calcConditional(add, dep, "", depNegative)
				second = calcConditional(node, add, nodeNegative, "~")
				prob2 = calcConditional(add, dep, "~", depNegative)

				return (first*prob1) + (second*prob2)

			else:
				if (nodeNegative == "~"):
					return 1 - node.condProb
				return node.condProb
		#in the case of diognostic 
		#preform the following values
		elif (reason == evidence["Diognostic"]):
			val= calcConditional(dep, node, depNegative, "")
			val *= node.condProb
			
			con = dep.condProb

			if (depNegative == "~"):
				con= 1-con
			val/= con

			if (nodeNegative == "~"):
				return (1-val)
			else:
				return val

		

#calculate the joint probability based on the conditional probability
def findJoint2(node, dep, nodeNegative, depNegative):
		if(depNegative == "~"):
			return (1-dep.condProb)* calcConditional(node, dep, nodeNegative, depNegative)
		elif(depNegative!="~"):
			return (dep.condProb)* calcConditional(node, dep, nodeNegative, depNegative)
#in the case we are dealing with a double debendencies
#We only need to confirm the value in the table
#no further computations are required
def calcConditional3(node,dep1,dep2,nodeNegative,dep1Negative,dep2Negative):
	if(node.probs.has_key(dep1Negative+dep1.appr+dep2Negative+dep2.appr)):
		result=node.probs.get(dep1Negative+dep1.appr+dep2Negative+dep2.appr)
	elif(node.probs.has_key(dep2Negative+dep2.appr+dep1Negative+dep1.appr)):
		result=node.probs.get(dep2Negative+dep2.appr+dep1Negative+dep1.appr)
	elif(((dep2.appr=="C" and dep1.appr=="S") or (dep1.appr=="C" and dep2.appr=="S")) and (dep2Negative=="" and dep1Negative=="")):
		if(nodeNegative==""):
			if(node.appr=="P"):
				return 0.156
			elif(node.appr=="S"):
				return 1
			elif(node.appr=="C"):
				return 1
			elif(node.appr=="X"):
				return 0.9
			elif(node.appr=="D"):
				return 0.65
		elif(nodeNegative=="~"):
			if(node.appr=="P"):
				return 1-0.156
			elif(node.appr=="S"):
				return 1-1
			elif(node.appr=="C"):
				return 1-1
			elif(node.appr=="X"):
				return 1-0.9
			elif(node.appr=="D"):
				return 1-0.65
	elif(((dep2.appr=="S" and dep1.appr=="D") or (dep1.appr=="S" and dep2.appr=="D")) and (dep2Negative=="" and dep1Negative=="")):
		if(nodeNegative==""):
			if(node.appr=="P"):
				return 0.102
			elif(node.appr=="S"):
				return 1
			elif(node.appr=="C"):
				return 0.067
			elif(node.appr=="X"):
				return 0.247
			elif(node.appr=="D"):
				return 1
		elif(nodeNegative=="~"):
			if(node.appr=="P"):
				return 1-0.102
			elif(node.appr=="S"):
				return 1-1
			elif(node.appr=="C"):
				return 1-0.067
			elif(node.appr=="X"):
				return 1-0.247
			elif(node.appr=="D"):
				return 1-1
	else:
		return
	if(nodeNegative=="~"):
		return float(1-result)
	elif(nodeNegative !="~"):
		return result
#compute the value of the joint funciton
#only if the values are related 
#check for the relation
def findJoint3(node,dep1,dep2,nodeNegative,dep1Negative,dep2Negative):
	x=calcConditional3(node,dep1,dep2,nodeNegative,dep1Negative,dep2Negative)
	y=calcConditional(dep1,dep2,dep1Negative,dep2Negative)

	if (dep2Negative == "~"):

		return float((1-dep2.condProb))*(x*y)
	else:
		return float(dep2.condProb)*(x*y)
			

	

def constructNet():
	P = BayesNode("Pollution", "P")
	S = BayesNode("Smoker", "S")
	C = BayesNode("Cancer", "C")
	D = BayesNode("Dyspnoea", "D")
	X = BayesNode("X-Ray", "X")
	P.setProb("P", 0.9)
	S.setProb("S", 0.3)
	S.setProb("S", 0.3)

	C.setProb("~PS", 0.05)
	C.setProb("~P~S", 0.02)
	C.setProb("PS", 0.03)
	C.setProb("P~S", 0.001)

	X.setProb("C", 0.9)
	X.setProb("~C", 0.2)

	D.setProb("C", 0.65)
	D.setProb("~C", 0.3)
	C.setParent(P)
	P.setChild(C)
	C.setParent(S)
	S.setChild(C)
	X.setParent(C)
	C.setChild(X)
	D.setParent(C)
	C.setChild(D)
	BayesNetwork["Pollution"]=P
	BayesNetwork["Smoker"]=S
	BayesNetwork["Cancer"]=C
	BayesNetwork["Dyspnoea"]=D
	BayesNetwork["X-Ray"]=X
	#find the conditional probability for each 
	#node
	for n in BayesNetwork.values():
			if n.condProbCalc == False:
				findConditional(n)

	
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    constructNet()
    for o, a in opts:
		if o in ("-p"):
			if(len(a)<2 or len(a)>6):
				print "This cannot  be updated"
				print "Either too many values or no values"
				sys.exit(0)
			print float(a[1:])
			if(float(a[1:])>1):
				print "No probability can be greater than 1 "
				sys.exit(0)
			setPrior(a[0], float(a[1:]))
			#setting the prior here works if the Bayes net is already built
			
		elif o in ("-m"):
			print "flag", o
			print "args", a
			print type(a)
			n=a.find("~")
			
			if(len(a)>1 and n==-1):
				print "Two values are not accepted for this"
				sys.exit(0)
			if(n!=-1):
				if(a[1].isupper()):
					print "Remove the negative format first"
					sys.exit(0)
			elif(len(a)>2):
				print "Two values are not accepted for this"
				sys.exit(0)
		
			result = None
			
			if (a.isupper()):
				if(exists(a)):
					result = find(a).condProb
				
				print("The Marginal Distribution of {} is: {}={} and ~{}={}").format(a.upper(),a.lower(),result,a.lower(),1-result)
			else:	
				
				if(n!=-1):
					result = find(a[1]).condProb
					print("The Marginal probability of {} is:{} ").format(a[1].lower(),1-result)
				else:
					result = find(a).condProb
					print("The Marginal probability of {} is:{} ").format(a.lower(),result)
			
			
			#calcMarginal(a)
		elif o in ("-g"):
			'''you may want to parse a here and pass the left of |
			and right of | as arguments to calcConditional
			if((not exists(node.appr.lower())) or not exists(dep.appr.lower())):
			print "This value is not correct and can't compute it"
			sys.exit(0)
			'''
			p = a.find("|")
			if(p==-1):
				print "Conditional must have the | symbol"
				sys.exit(0)
			else:
				listS = {}
				#In case we have a value that is upper case make sure we consider
				#Both cases of positive and negative values
				convertDistribution(a, listS)

				for arg in listS.keys():
					p=arg.find("|")
					node=arg[:p]
					nodeNegative = ""
					if(node.find("~")!=-1):
						node = node[1]
						nodeNegative = "~"

					dep = []
					depNegative = []

					n = False
					conditions=arg[p+1:]
					for value in conditions:
						if(value != "~"):
							dep.append(value)
							#print(reasonOfEvidence(find(node),find(value)))
						elif(value=="~"):
							n=True
							
						if(n == True):
							n = False
							depNegative.append("~")
						else:
							depNegative.append("")
					if(len(dep)==1):
						if(exists(dep[0]) and exists(node)):
							print("conditional probability of  {} is {}").format(arg,calcConditional(find(node),find(dep[0]),nodeNegative,depNegative[0]))
						else:
							print "No Such value"
							sys.exit(0)
					elif(len(dep)==2):
						if(exists(dep[0]) and exists(node) and exists(dep[1])):
							if(len(depNegative)>3):
								if(calcConditional3(find(node),find(dep[0]),find(dep[1]),nodeNegative,depNegative[0],depNegative[2])!=None):
									print("Conditional probability of {} is {}").format(arg,calcConditional3(find(node),find(dep[0]),find(dep[1]),nodeNegative,depNegative[0],depNegative[2]))
							elif(len(depNegative)<=3):
								if(calcConditional3(find(node),find(dep[0]),find(dep[1]),nodeNegative,depNegative[0],depNegative[1])!=None):
									print("The Conditional probability of {} is {}").format(arg,calcConditional3(find(node),find(dep[0]),find(dep[1]),nodeNegative,depNegative[0],depNegative[1]))
						else:
							print "One or more arguments are not available"
							sys.exit(0)
			#calcConditional(a[:p], a[p+1:])
		elif o in ("-j"):
			print "flag", o
			print "args", a
			p = a.find("|")
			if(p!=-1):
				print "This probability is not a joint Probability"
				sys.exit(0)
			elif(len(a)<2 or len(a)>3):
				print "Calculations cannot be preformed"
				sys.exit(0)
			else:
				listS = {}
				convertDistribution(a, listS)
				print "here is the list"
				print(listS.keys())
				for arg in listS.keys():
					nodes = []
					nodesNegative = []

					n = False
					for c in arg:
						if c == "~":
							n = True
						else:
							nodes.append(c)
						if n == True:
							n = False
							nodesNegative.append("~")
						else:
							nodesNegative.append("")
				print(nodes)
				print(nodesNegative)
				if(len(nodes)==2):
					if(exists(nodes[0]) and exists(nodes[1])):
						print("joint probability of  {} is {}").format(arg,findJoint2(find(nodes[0]),find(nodes[1]),nodesNegative[0],nodesNegative[1]))
					else:
						print "No Such value"
						sys.exit(0)
				elif(len(nodes)==3):
					if(exists(nodes[0]) and exists(nodes[1]) and exists(nodes[2])):
						print("Joint probability of {} is {}").format(arg,findJoint3(find(nodes[0]),find(nodes[1]),find(nodes[2]),nodesNegative[0],nodesNegative[1],nodesNegative[2]))
					else:
						print "No such value"
						sys.exit(0)
				
				
					


	
				
		else:
			assert False, "unhandled option"
		
    # ...

if __name__ == "__main__":
    main()
