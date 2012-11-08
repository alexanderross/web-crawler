import urllib
import webparse 
import sqlgen


root="http://www.sportslogos.net/"
wp = webparse.webparse()
sq = sqlgen.sqlgen('output.sql')
res =wp.getPageContent(root," <li class=\"headingFont title\">","<a ",False)

resPro=wp.processArray(res,["href","title"],["ISOLATE>>league_id=>href.by_league/*/","ISOLATE>>category_id=>href.by_category/*/","CATEGORIZE=>title.list_by_category"],[" Logos"])
p = len(resPro)
print(str(p)+ " Inital Categories. Digging deeper.")
i=0

for result in resPro:
	i=i+1
	temp=wp.getPageContent(root+result[0][1],"<ul class=\"logoWall\">","<a ",False)
	wp.current_cat=""
	tempy=wp.processArray(temp,["href","title","src"],["DENY=>#top","ISOLATE>>team_id=>href.team/*/","ISOLATE>>image_code=>src.thumbs/*.gif"],[" Logos"])
	print tempy
	sq.write_single(result)
	sq.write(tempy)
	print(str(i)+" of "+str(p)+" done.")
	
sq.makeSQL()
	
	





	



