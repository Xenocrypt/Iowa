import json
import urllib2
VoteList = []
VoteListIDs = []
VoteDict = {}
APIKEY = '2e7d7ececfb742cf9f8394c300e98616'
HouseBillList =  json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=MD&chamber=lower&search_window=session:2013&apikey=%s' % (APIKEY)))
SenateBillList = json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/?state=MD&chamber=upper&search_window=session:2013&apikey=%s' % (APIKEY)))
for x in HouseBillList+SenateBillList:
    Votes = json.load(urllib2.urlopen('http://openstates.org/api/v1/bills/md/%s/%s/%s/?apikey=%s' % (urllib2.quote(x['session']), urllib2.quote(x['chamber']), urllib2.quote(x['bill_id']), APIKEY)))['votes']
    if len(Votes) > 0:
        for Vote in Votes:
            if Vote['session'] == '2013-2014' and Vote['yes_count'] > 0 and Vote['no_count'] > 0:
                VoteList.append(Vote)
                VoteListIDs.append(Vote['vote_id'])
                for Legislator in list(Vote['yes_votes'])+list(Vote['no_votes']):
                    if Legislator['leg_id'] not in VoteDict:
                         VoteDict[Legislator['leg_id']] = {'Name': Legislator['name']}  
                print Vote['date'], len(VoteList)                     
Length = len(VoteList)
VoteCodes = {'yes_votes': 1, 'no_votes': 6}
for i in range(len(VoteList)):
    Vote = VoteList[i]
    for Option in VoteCodes:
        for Legislator in Vote[Option]:
            if 'Votes' not in VoteDict[Legislator['leg_id']]:
                VoteRow = []
                while len(VoteRow) < len(VoteList):
                    VoteRow.append(9)
                VoteDict[Legislator['leg_id']]['Votes'] = VoteRow
            VoteDict[Legislator['leg_id']]['Votes'][i] = VoteCodes[Option]
j = '1'
k = '1'
def StateDifferenceFinder(j, k):
    First = VoteDict[j]['Votes']
    Second = VoteDict[k]['Votes']
    Difference = []
    for L in range(len(VoteList)):
        Max = max(First[L], Second[L])
        Min = min(First[L], Second[L])
        if Max-Min == 5:
            print VoteList[L]['vote_id']
            Difference.append(VoteList[L]['vote_id'])
    return Difference  
    
            
    
