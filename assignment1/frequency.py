import sys
import json
def fequeryReader(pf):
    frquencyList = {}
    for line in pf:
      tweet = json.loads(line)
      if 'text' in tweet.keys():
          text = tweet['text']
          wordList = text.encode('utf-8').lower().split()
          for word in wordList:
               if word in frquencyList.keys():
                   frquencyList[word] = frquencyList[word] + 1
               else:
                   frquencyList[word] = 1
    return frquencyList


def main():
    tweet_file = open(sys.argv[1])
    frequencyList = fequeryReader(tweet_file)
    for key in frequencyList:
        print key, round(float(float(frequencyList[key]) / len(frequencyList)), 4)

if __name__ == '__main__':
    main()
