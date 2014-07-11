import sys
import json

def readScores(fb):
    scores = {};
    for line in fb:
        term, score = line.split("\t")
        scores[term] = int(score)
    return scores
def readTweetsText(fb, scores):
    tweetslist = []
    for line in fb:
        sentiment = 0
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            text = tweet['text']
            wordList = text.encode('utf-8').lower().split()
            for value in wordList:
                 if value in scores.keys():
                     sentiment = sentiment + scores[value]
        tweetslist.append(sentiment)
    return tweetslist
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = readScores(sent_file)
    tweetslist = readTweetsText(tweet_file, scores)
    for val in tweetslist:
        print val

if __name__ == '__main__':
    main()
