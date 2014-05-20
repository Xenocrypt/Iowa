import json
import csv
Relationships = csv.reader(open('ia19trf.txt'))
List = [csv.reader(open('DEC_00_SF3_DP2_with_ann.csv')), csv.reader(open('ACS_12_5YR_DP02_with_ann.csv'))]
Dicts = {}
Years = ['2000', '2012']
Indexes = {'2000': {'Pop25+': 15, 'Pop': 93, 'Pop25+BA': 27, 'Pop25+Grad': 29}, '2012': {'Pop25+': 231, 'Pop25+BA': 255, 'Pop25+Grad': 259, 'Pop': 487}}
IowaTracts = json.load(open('IATracts.json'))
Dict2000 = {}
Dict2012 = {}
for i in range(2):
	for x in List[i]:
		if x[0] != 'GEO.id':
			Dicts[x[1]+'-'+Years[i]] = {}
			for y in Indexes[Years[i]]:
				Dicts[x[1]+'-'+Years[i]][y] = float(x[Indexes[Years[i]][y]])
Tree = {}
def FindRoot(i):
	Root = Tree[i]
	while Root != Tree[Root]:
		Root = Tree[Root]
	return Root
for x in Relationships:
	if x[-6] != '0':
		Tuple = (x[3]+'-2000', x[12]+'-2012')
		if Tuple[0] not in Tree and Tuple[1] not in Tree:
			Tree[Tuple[0]] = max(Tuple)
			Tree[Tuple[1]] = max(Tuple)
		if Tuple[0] in Tree and Tuple[1] not in Tree:
			Tree[Tuple[1]] = Tuple[0]
		if Tuple[1] in Tree and Tuple[0] not in Tree:
			Tree[Tuple[0]] = Tuple[1]
		if Tuple[1] in Tree and Tuple[0] in Tree:
			MaxRoot = max(FindRoot(Tuple[1]), FindRoot(Tuple[0]))
			Tree[FindRoot(Tuple[1])] = MaxRoot
			Tree[FindRoot(Tuple[0])] = MaxRoot
Clusters = {}
for x in Tree:
	for z in Indexes[x[-4:]]:
		if FindRoot(x) not in Clusters:
			Clusters[FindRoot(x)] = {}
		if z+'-'+x[-4:] not in Clusters[FindRoot(x)]:
			Clusters[FindRoot(x)][z+'-'+x[-4:]] = 0.0
		Clusters[FindRoot(x)][z+'-'+x[-4:]] = Clusters[FindRoot(x)][z+'-'+x[-4:]]+Dicts[x][z]
for x in IowaTracts['features']:
	try:
		for z in Clusters[FindRoot(x['properties']['GEOID']+'-2012')]:
			x['properties'][z] = Clusters[FindRoot(x['properties']['GEOID']+'-2012')][z]
	except:
		for y in Indexes:
			for z in Indexes[y]:
				x['properties'][z+'-'+y] = 0.0
with open("IATractsEdited.json", 'wb') as file:
	json.dump(IowaTracts, file)
