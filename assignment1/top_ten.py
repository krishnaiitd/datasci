import sys
import json
def top10Reader(pf):
    frquencyList = {}
    for line in pf:
      tweet = json.loads(line)
      if 'entities' in tweet.keys():
          entities = tweet['entities']
          if entities['hashtags']:
              if entities['hashtags'][0]['text'] in frquencyList.keys():
                  frquencyList[entities['hashtags'][0]['text']] = frquencyList[entities['hashtags'][0]['text']] + 1
              else:
                  frquencyList[entities['hashtags'][0]['text']] = 1;

    topFrquencyList = sorted(frquencyList.items(), key=lambda x:x[1], reverse=True)
    #print topFrquencyList
    top10FrquencyList = topFrquencyList[0:10]
    return top10FrquencyList
def main():
    tweet_file = open(sys.argv[1])
    top10FrquencyList = top10Reader(tweet_file)
    for values in top10FrquencyList:
        print values[0], values[1]

if __name__ == '__main__':
    main()
