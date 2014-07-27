import urllib2,re

div2Pos = 0
res = []
RoundID = "16009"
pointDiv1 = [250, 500, 1000]
pointDiv2 = [250, 500, 1000]
pointEasy = []
def jump(pos, allInfo, aim, times):
	for i in xrange(times):
		npos = allInfo[pos:].find(aim)
		pos += npos + len(aim) + 1
	return pos

def getNextPoint(pos, allInfo):
	pp = ""
	while allInfo[pos] != '>':
		pos += 1
	pos += 1
	if allInfo[pos] == '<':
		while allInfo[pos] != '>':
			pos += 1
		pos += 1
	while allInfo[pos] != '<':
		pp += allInfo[pos]
		pos += 1
	return pp

def outOfCompetition(userId):
	coder = []
	coder.append(userId)
	coder.append("-1")
	coder.append("-10000.00")
	coder.append("0")
	coder.append("0")
	coder.append("0.00")
	coder.append("0.00")
	coder.append("0.00")
	coder.append("-10000.00")
	coder.append("OutOfCompetition!")
	res.append(coder)

def GetInfo(userId, allInfo):
	allPoint = ""
	easyPoint = ""
	mediumPoint = ""
	hardPoint = ""
	successHack = ""
	unsuccessHack = ""
	nowpos = allInfo.find(userId)
	if nowpos == -1:
		outOfCompetition(userId)
		return
	nowpos = jump(nowpos, allInfo, "onclick", 1)
	allPoint = getNextPoint(nowpos, allInfo)
	nowpos = jump(nowpos, allInfo, "tooltip", 1)
	easyPoint = getNextPoint(nowpos, allInfo)
	nowpos = jump(nowpos, allInfo, "tooltip", 1)
	mediumPoint = getNextPoint(nowpos, allInfo)
	nowpos = jump(nowpos, allInfo, "tooltip", 1)
	hardPoint = getNextPoint(nowpos, allInfo)
	nowpos = jump(nowpos, allInfo, "</td><td>", 1)
	nowpos -= 2
	successHack = getNextPoint(nowpos, allInfo)
	nowpos = jump(nowpos, allInfo, "</td><td>", 1)
	nowpos -= 2
	unsuccessHack = getNextPoint(nowpos, allInfo)
	coder = []
	coder.append(userId)
	coder.append("-1")
	coder.append(allPoint)
	coder.append(successHack)
	coder.append(unsuccessHack)
	coder.append(easyPoint)
	coder.append(mediumPoint)
	coder.append(hardPoint)
	coder.append("0")
	if nowpos < div2Pos:
		coder.append("Div.1")
	else:
		pointEasy.append(float(easyPoint))
		coder.append("Div.2")
	res.append(coder)

def Print():
	global res
	averagePointEasy = 0.0
	for i in xrange(min(10, len(pointEasy))):
		averagePointEasy += pointEasy[i]
	averagePointEasy /= min(10, len(pointEasy))

	for i in res:
		if i[9] == "Div.1":
			i[5] = str(float(i[5]) * pointDiv2[1] / pointDiv1[0])
			i[6] = str(float(i[6]) * pointDiv2[2] / pointDiv1[1])
			i[7] = str(float(i[7]) * 5)
			i[8] = str(averagePointEasy)
			i[2] = str(float(i[5]) + float(i[6]) + float(i[7]) + float(i[8]) + 50 * int(i[3]) - 25 * int(i[4]))
	
	print "handle	Rank	Score	+	-	Easy	Medium	Hard	Bouns	Div"
	res.sort(lambda x,y : -cmp(float(x[2]), float(y[2])))
	cnt = 0
	lastcnt = 1
	last = -1
	for i in res:
		if last == float(i[2]):
			lastcnt = lastcnt + 1
		else:
			cnt = cnt + lastcnt
			lastcnt = 1
		last = float(i[2])
		i[1] = str(cnt)
		This = ""
		for j in i:
			This += j + "	"
		print This

IDlist = open("idlistTC.txt")
line = IDlist.readline()
URL = "http://ahmed-aly.com/TopCoderTools/NewScoreboard.jsp?RoundID=" + RoundID + "&division=3&Countries=&Country=&Schools=&School=&level_one_status=All&level_two_status=All&level_three_status=All&Solved=Any&ScoreAtLeast=&ScoreAtMost=&Handles=&Handle=&TopAtLeast=&Top=&OldRateAtLeast=&OldRateAtMost=&RateAtLeast=&RateAtMost="
req = urllib2.Request(URL)
# print req
while True:
	try:
		response = urllib2.urlopen(req)
		# print response
		break
	except Exception, data:
		print data
		print "FUCK"
result = response.read()
div2Pos = result.find("SRM 628 Division 2 Scoreboard")
# print result
# while line:
while line:
	GetInfo(line[:len(line)-1], result)
	line = IDlist.readline()

Print()