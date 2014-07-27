import urllib2,re

res = []

assign = {}

def Print():
	global res
	global assign
	for (k,v) in assign.items():
		if v == 0:
			coder = []
			coder.append(k)
			coder.append("INF")
			coder.append("-10000")
			for i in xrange(7):
				coder.append("0")
			coder.append("-10000")
			coder.append("OutOfCompetition!")
			res.append(coder)

	print "handle	Rank	Score	+	-	A	B	C	D	E	Bouns	Div"
	res.sort(lambda x,y : -cmp(int(x[2]), int(y[2])))
	cnt = 0
	lastcnt = 1
	last = -1
	for i in res:
		if last == int(i[2]):
			lastcnt = lastcnt + 1
		else:
			cnt = cnt + lastcnt
			lastcnt = 1
		last = int(i[2])
		i[1] = str(cnt)
		This = ""
		for j in i:
			This += j + "	"
		print This


contestId = "451"
contestIdDiv1 = ""
apiURLhead = "http://codeforces.com/api/contest.standings?showUnofficial=true&contestId="
apiURLtail = "&handles="
IDlist = open("idlistCF.txt")
line = IDlist.readline()
flag = 0


while line:   # Get all IDs and insert in URL
	if flag == 0:
		apiURLtail = apiURLtail + line[0:len(line)-1]
	else:
		apiURLtail = apiURLtail + ";" + line[0:len(line)-1]
	assign[line[0:len(line)-1]] = 0
	flag = 1
	line = IDlist.readline()

apiURL = apiURLhead + contestId + apiURLtail

req = urllib2.Request(apiURL)

# print apiURL

while True: #Try to connect
	try:
		response = urllib2.urlopen(req)
		break
	except Exception, data:
		print data

# print apiURL


fullPointDiv2 = []
averagePointDiv2A = 0
averagePointDiv2B = 0
competitors = 0

result = response.read()
nowpos = 0

for i in xrange(5):    #Get the full point in Div.2
	nxtpos = result[nowpos:].find("points")
	nxtpos += 8 + nowpos
	pointnow = 0
	while result[nxtpos] != '.':
		pointnow = pointnow * 10 + int(result[nxtpos])
		nxtpos += 1
	nowpos = nxtpos
	fullPointDiv2.append(pointnow)

# print fullPointDiv2

while True:
	nxtpos = result[nowpos:].find("handle") # Get handle
	if nxtpos == -1:
		break
	nxtpos += 9 + nowpos
	handle = ""
	while result[nxtpos] != '"':
		handle += result[nxtpos]
		nxtpos += 1
	nowpos = nxtpos

	nxtpos = result[nowpos:].find("participantType")  #Get participanttype
	# print nxtpos
	nxtpos += 18 + nowpos
	Type = ""
	while result[nxtpos] != '"':
		Type += result[nxtpos]
		nxtpos += 1
	nowpos = nxtpos
	if Type == "VIRTUAL" or Type == "PRACTICE":
		continue
	competitors += 1
	coder = []
	coder.append(handle)
	assign[handle] = 1
	nxtpos = result[nowpos:].find("rank")  #Get rank
	nxtpos += 6 + nowpos
	rank = ""
	while result[nxtpos] != ',':
		rank += result[nxtpos]
		nxtpos += 1
	nowpos = nxtpos 
	coder.append(rank)
	# print nowpos

	nxtpos = result[nowpos:].find("points")  #Get point
	nxtpos += 8 + nowpos
	point = ""
	while result[nxtpos] != '.':
		point += result[nxtpos]
		nxtpos += 1
	nowpos = nxtpos 
	coder.append(point)

	nxtpos = result[nowpos:].find("successfulHackCount")  #Get SuccessHack
	nxtpos += 21 + nowpos
	SuccessHack = ""
	while result[nxtpos] != ',':
		SuccessHack += result[nxtpos]
		nxtpos += 1
	nowpos = nxtpos 
	coder.append(SuccessHack)

	nxtpos = result[nowpos:].find("unsuccessfulHackCount")  #Get UnsuccessHack
	nxtpos += 23 + nowpos
	UnsuccessHack = ""
	while result[nxtpos] != ',':
		UnsuccessHack += result[nxtpos]
		nxtpos += 1
	nowpos = nxtpos 
	coder.append(UnsuccessHack)

	for j in xrange(5):
		nxtpos = result[nowpos:].find("points")  #Get point for 5 problems 
		nxtpos += 8 + nowpos
		point = ""
		while result[nxtpos] != '.':
			point += result[nxtpos]
			nxtpos += 1
		nowpos = nxtpos 
		coder.append(point)
	# print coder
	coder.append("0")
	coder.append("Div.2")
	res.append(coder)
	# break

if contestIdDiv1 == "":
	Print()
else:
	res.sort(lambda x,y : -cmp(int(x[5]), int(y[5])));
	competitorsA = 0

	for i in res:
		if int(i[5]) > 0:
			averagePointDiv2A += int(i[5])
			competitorsA += 1
		if competitorsA == 10:
			break

	res.sort(lambda x,y : -cmp(int(x[6]), int(y[6])));

	competitorsB = 0
	for i in res:
		# print int(i[6])
		if int(i[6]) > 0:
			averagePointDiv2B += int(i[6])
			competitorsB += 1
		if competitorsB == 10:
			break

	# print averagePointDiv2A, averagePointDiv2B, competitorsA, competitorsB
	
	averagePointDiv2B /= competitorsB
	averagePointDiv2A /= competitorsA



	apiURL = apiURLhead + contestIdDiv1 + apiURLtail

	req = urllib2.Request(apiURL)

	# print apiURL

	while True:
		try:
			response = urllib2.urlopen(req)
			break
		except Exception, data:
			print data

	# print apiURL

	result = response.read()

	fullPointDiv1 = []
	nowpos = 0

	for i in xrange(5):    #Get the full point in Div.1
		nxtpos = result[nowpos:].find("points")
		nxtpos += 8 + nowpos
		pointnow = 0
		while result[nxtpos] != '.':
			pointnow = pointnow * 10 + int(result[nxtpos])
			nxtpos += 1
		nowpos = nxtpos
		fullPointDiv1.append(pointnow)

	# print fullPointDiv1

	while True:
		nxtpos = result[nowpos:].find("handle") # Get handle
		if nxtpos == -1:
			break
		nxtpos += 9 + nowpos
		handle = ""
		while result[nxtpos] != '"':
			handle += result[nxtpos]
			nxtpos += 1
		nowpos = nxtpos

		nxtpos = result[nowpos:].find("participantType")  #Get participanttype
		# print nxtpos
		nxtpos += 18 + nowpos
		Type = ""
		while result[nxtpos] != '"':
			Type += result[nxtpos]
			nxtpos += 1
		nowpos = nxtpos
		if Type == "VIRTUAL" or Type == "PRACTICE":
			continue
		competitors += 1
		coder = []
		assign[handle] = 1
		nxtpos = result[nowpos:].find("rank")  #Get rank
		nxtpos += 6 + nowpos
		rank = ""
		while result[nxtpos] != ',':
			rank += result[nxtpos]
			nxtpos += 1
		nowpos = nxtpos 
		# print nowpos

		nxtpos = result[nowpos:].find("successfulHackCount")  #Get SuccessHack
		nxtpos += 21 + nowpos
		SuccessHack = ""
		while result[nxtpos] != ',':
			SuccessHack += result[nxtpos]
			nxtpos += 1
		nowpos = nxtpos 

		nxtpos = result[nowpos:].find("unsuccessfulHackCount")  #Get UnsuccessHack
		nxtpos += 23 + nowpos
		UnsuccessHack = ""
		while result[nxtpos] != ',':
			UnsuccessHack += result[nxtpos]
			nxtpos += 1
		nowpos = nxtpos 

		pointAll = 0
		pointnow = []
		for j in xrange(5):
			nxtpos = result[nowpos:].find("points")  #Get point for 5 problems 
			nxtpos += 8 + nowpos
			point = ""
			while result[nxtpos] != '.':
				point += result[nxtpos]
				nxtpos += 1
			nowpos = nxtpos
			if j == 0:
				point = str(int(int(point) * ((fullPointDiv2[2]+0.0)/fullPointDiv1[0])))
			elif j == 1:
				point = str(int(int(point) * ((fullPointDiv2[3]+0.0)/fullPointDiv1[1])))
			elif j == 2:
				point = str(int(int(point) * ((fullPointDiv2[4]+0.0)/fullPointDiv1[2])))
			elif j == 3:
				point =	str(int(point) * 3)
			else:
				point = str(int(point) * 5)
			pointAll += int(point)
			pointnow.append(point)
		# print pointnow
		pointAll += int(SuccessHack) * 100
		pointAll -= int(UnsuccessHack) * 50
		pointAll += averagePointDiv2B + averagePointDiv2A
		coder.append(handle)
		coder.append(rank)
		coder.append(str(pointAll))
		coder.append(SuccessHack)
		coder.append(UnsuccessHack)
		for i in pointnow:
			coder.append(i)
		coder.append(str(averagePointDiv2A + averagePointDiv2B))
		coder.append("Div.1")
		res.append(coder)
		# print coder
		# break



	# print res[1]

	Print()
