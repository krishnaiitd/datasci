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
    nonSentiment = {}
    for line in fb:
        sentiment = 0
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            text = tweet['text']
            wordList = text.encode('utf-8').lower().split()
            for value in wordList:
                 if value in scores.keys():
                     sentiment = sentiment + scores[value]
                 else :
                     if value in nonSentiment.keys():
                         nonSentiment[value] = nonSentiment[value] + 1;
                     else:
                         nonSentiment[value] = 1
        tweetslist.append(sentiment)
    index = 0;
    nonSentimentScore = {}
    fb.seek(0,0)
    for line in fb :
        tweet = json.loads(line)
        if 'text' in tweet.keys():
            text = tweet['text']
            wordList = text.encode('utf-8').lower().split()
            for value in wordList:
                 if value not in scores.keys():
                     nonSentimentScore[value] =  value + ' ' + str((tweetslist[index])/ (nonSentiment[value]))
        index = index+1
    return nonSentimentScore
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    scores = readScores(sent_file)
    nonSentimentScore = readTweetsText(tweet_file, scores)
    for value in nonSentimentScore:
        print nonSentimentScore[value].split()


if __name__ == '__main__':
    main()
