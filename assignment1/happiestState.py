import sys
import json

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
def fequeryReader(pf):
    frquencyList = {}
    for line in pf:
      tweet = json.loads(line)
      if 'lang' in tweet.keys():
          if tweet['lang'] != 'en':
              continue;
      if 'text' in tweet.keys():
          text = tweet['text']
          wordList = text.encode('utf-8').lower().split()
          for word in wordList:
               if word in frquencyList.keys():
                   frquencyList[word] = frquencyList[word] + 1
               else:
                   frquencyList[word] = 1
    return frquencyList
def readScores(fb):
    scores = {};
    for line in fb:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores
def readTweetsText(fb, scores):
    stateTweetCount = {}
    stateTweetValues = {}
    for line in fb:
        sentiment = 0
        state = ''
        statekey = ''
        tweet = json.loads(line)
        if 'lang' in tweet.keys():
            if tweet['lang'] != 'en':
                continue;
        if 'user' not  in tweet.keys():
            continue
        location = tweet['user']['location']
        #print location
        if  location in states.values():
            #print 'Found in values== ', location
            state = location
        if location in states.keys():
            #print 'Found in key== ', location
            statekey = location
        if statekey is '' or state is '':
            locationlist = location.split(',')
            for value in locationlist:
                if value.strip() in states.values():
                    #print 'Found in values== ', value.strip()
                    state = value.strip()
                if value.strip() in states.keys():
                    #print 'Found in keys== ', value.strip()
                    statekey = value.strip()
        if statekey is '' and state is not '':
            statekey = list(states.keys())[list(states.values()).index(state)]
        if statekey is '' or not statekey:
            continue

        ## find the sum of the sentiment values of the tweet
        if 'text' in tweet.keys():
            text = tweet['text']
            wordList = text.encode('utf-8').lower().split()
            for value in wordList:
                 if value in scores.keys():
                     sentiment = sentiment + int(scores[value])

        #print statekey, sentiment
        if statekey in stateTweetValues.keys():
            stateTweetValues[statekey] = stateTweetValues[statekey] + sentiment
            stateTweetCount[statekey] = stateTweetCount[statekey] + 1
        else:
            stateTweetValues[statekey] = sentiment
            stateTweetCount[statekey] = 1
    #print stateTweetValues
    #print stateTweetCount
    return stateTweetValues,stateTweetCount
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = readScores(sent_file)
    stateTweetValues,stateTweetCount = readTweetsText(tweet_file, scores)
    stateTweetAvg = {}
    for values in stateTweetValues:
        #print values, stateTweetValues[values], stateTweetCount[values]
        stateTweetAvg[values] = round(float(stateTweetValues[values])/stateTweetCount[values], 2)
    sortedList = sorted(stateTweetAvg.items(), key=lambda x:x[1], reverse=True)
    if len(sortedList) > 0:
        happy_state = sortedList[0][0]
        sys.stdout.write(str(happy_state))
        sys.stdout.flush()
    else:
        sys.stdout.write("There is no happiest state with a 2 letter length, I wonder what gives?")
        sys.stdout.flush()
if __name__ == '__main__':
    main()
