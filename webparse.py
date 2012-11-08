import urllib
from array import *


class webparse:
	current_cat=""
	current_isolate=[]
	newCat=False
	tagTypes=["div","body","html","td","tr","table","label","bold","center","a","li","ul"]
	def __init__(self):
		pass
	
	def getPageContent(self,url,start,sub,recurse):
		sock = urllib.urlopen(url)
		content = sock.read() 
		content = content.split("\n")
		sock.close()
		return self.filterpage(content,start,sub)
	
	def filterpage(self,content,start,sub):
		started = False
		markerCount=0
		returnArray=[]
		marker = self.getMarker(start)
		submarker = self.getMarker(sub)
		subLine = ""
		for line in content:
			markerCount = markerCount + line.count("<"+marker+" ")
			markerCount = markerCount - line.count("</"+marker)
			if(line.find(start) > -1):
					started=True
			if(started):
				if(markerCount==0):
					started=False
				if(line.count("<"+submarker+" ")>0):
					subLine=line.split("<"+submarker+" ")[1]
					if(line.count("</"+submarker)>0):
						returnArray.append(subLine.split("</"+submarker)[0].replace("\n","").replace("  ",""))
						subLine=""
				elif(subLine != ""):
					if(line.count("</"+submarker)>0):
						subLine= subLine + line.split("</"+submarker)[0]
						returnArray.append(subLine.replace("\n","").replace("	",""))
						subLine=""
					else:
						subLine = subLine+line

		return returnArray
					
	def getMarker(self,marker_context):
		for entry in self.tagTypes:
			if(marker_context.find("<"+entry+" ")>-1):
				return entry;
				
	def processArray(self,data,tags,filter,remove):
		returnArray=[]
		tempArray=[]
		for entry in data:
			temp =self.extractFields(entry,tags,filter,remove)
			if(not temp == "I"):
				if(self.current_cat !=""):
					temp.append(self.current_cat)
				for entry in self.current_isolate:
					temp.append(entry)
				self.current_isolate=[]
				returnArray.append(temp)
	
		return returnArray
			
	def extractFields(self,line,tags,filters,remove):
		for entry in remove:
			line=line.replace(entry,"")

		if(not self.shouldIgnore(line,filters)):
			return(self.evalFields(line,tags))
		else:
			return "I"
	
	def evalFields(self,line,tags):
		returnKVPs = []
		nextTag=""
		temp=line.split("\"");
		for part in temp:
			if(nextTag!=""):
				returnKVPs.append([nextTag,part])
				nextTag=""
			for tag in tags:
				if(part.find(tag)>=0):
					nextTag=tag
		return returnKVPs
			
	def processCat(self,line,attr):
		val = self.evalFields(line,[attr])
		
		self.current_cat = val[0][1]
		
	def processIsolate(self,line,attr,isoStart,isoEnd,isoTag):
		val = self.evalFields(line,[attr])	
		val[0][1] = val[0][1][val[0][1].find(isoStart)+len(isoStart):]
		val[0][1] = val[0][1][:val[0][1].find(isoEnd)]
		
		self.current_isolate.append([isoTag,val[0][1]])
		
	def shouldIgnore(self,line,filterVals):
		returnVal=True
		for val in filterVals:
			values=val.split("=>")
			if(values[0].find("ISOLATE")>=0):
				tag=values[0].split(">>")[1]
				delim =values[1].split("*")
				delim2 = delim[0].split(".")
				if(line.find(delim2[1]) >=0):
					self.processIsolate(line,delim2[0],delim2[1],delim[1],tag)
					returnVal= False
			elif(values[0]=="CATEGORIZE"):
				delim=values[1].split(".")
				if(line.find(delim[1]) >=0):
					self.processCat(line,delim[0])	
					returnVal= False
			elif(line.find(values[1]) >=0 ):
				if(values[0]=="ALLOW"):
					returnVal= False
					print "ALL"
				else:
					return True
		return returnVal
					
