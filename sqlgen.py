


class sqlgen:

	f=""
	current_cat_id=-1
	current_team_id=-1
	current_league_id=-1
	
	prepare_leagues=[]
	prepare_teams=[]
	prepare_cats=[]
	
	write_queue=[]
	def __init__(self,dest):
		self.f=open(dest,'w')
		
	def write(self,mylist):
		for entry in mylist:
			self.addToQueue(entry)

		
	def write_single(self,mySingleList):
		self.addToQueue(mySingleList)
		
	def addToQueue(self,entry):
		if(entry[0][1].find("list_by_league")>=0):
			if(entry[3][0].find("league_id")>=0):
				self.prepareLeagueSQL(entry)
		elif(entry[0][1].find("list_by_team")>=0):
			self.prepareTeamSQL(entry)
		elif(entry[0][1].find("list_by_category")>=0):
			self.prepareCatSQL(entry)
	
	
	def prepareTeamSQL(self,line):
		queryLine="INSERT INTO teams (id,name,wins,losses,rank,image_code,league_id,created_at,updated_at) VALUES ('"+line[3][1]+"','"+self.scrub_line(line[1][1])+"',0,0,0,'"+line[4][1]+"',"+str(self.current_league_id)+",now(),now());"
		self.prepare_teams.append(queryLine)
		
	def prepareCatSQL(self,line):
		queryLine="INSERT INTO team_categories (id,name,created_at,updated_at)VALUES('"+line[3][1]+"','"+self.scrub_line(line[1][1])+"',now(),now());"
		self.current_cat_id=line[3][1]
		self.prepare_cats.append(queryLine)

	def prepareLeagueSQL(self,line):
		queryLine="INSERT INTO leagues (id,category_id,name,created_at,updated_at)VALUES('"+line[3][1]+"',"+str(self.current_cat_id)+",'"+self.scrub_line(line[1][1])+"',now(),now());"
		self.current_league_id=line[3][1]
		self.prepare_leagues.append(queryLine)
	
	def scrub_line(self,line):
		return line.replace("'","")
			
	def makeSQL(self):
		for entry in self.prepare_cats:
			self.f.write(str(entry)+"\n")
		for entry in self.prepare_leagues:
			self.f.write(str(entry)+"\n")
		for entry in self.prepare_teams:
			self.f.write(str(entry)+"\n")
			