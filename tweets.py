import tweepy
from sentmentAnalisys import sentiment_scores, sentiment_scores_of_array
import nltk
from nltk.corpus import stopwords
from summa import keywords
from yake import yake


api_key = 'Z4M4N7zL0ubaam2opHmV9eFKf'
api_key_secret = 'jc1HsOTT9p6673kJM99BFzHC1UrqERKHk1OxQSlHOagt0g1OZp'
bearer_token  = 'AAAAAAAAAAAAAAAAAAAAAFeijgEAAAAAgZQQ%2Byq9yfV1ijZPM2b91qdrSu0%3DoMWg9mQ4wHLT04ah9nerTcweU99SjEldNckgZ1TluVzKjQZHF1'
access_token = "1595482520291885074-iN9vBxgoqFotubkiPzEQaRlEFE0kLo"
access_token_secret = "9rn0KEngcZIkLJZKvshuDgDeXBDdJB093P3mfRvZPOzWz"

client = tweepy.Client(bearer_token)



def removeStopWords(sentence):
    sentences = nltk.sent_tokenize(sentence)
    cleanSentences = ""
    for i in range(len(sentences)):
        words = nltk.word_tokenize(sentences[i])
        newwords = [word for word in words if word not in stopwords.words('portuguese')]
        sentences[i] = ' '.join(newwords)
    for sentence in sentences:
        cleanSentences = cleanSentences + cleanString(sentence) + " "
    return cleanSentences

def cleanString(word):
    punctuations = ['.', ',', '!', '?', ':', ';', '(', ')', '"', "'", "‘", "`", "´"]
    for punctuation in punctuations:
        word = word.replace(punctuation, '')
    splitedString = word.split(" ")
    formatedString = ""
    
    for token in splitedString:
        if len(token) > 5:
            formatedString = formatedString + token + " "
    return formatedString.strip()

def getTwetsOffAllNotices(notices):
    newsWithTweets = []
    tweets = []
    for notice in notices:
        tweets = getTweets(removeStopWords(notice['title']))
        newsWithTweets.append({
            "news": notice,
            "tweets": tweets,
            "generalSentmentAnalisys": getGeneralSentmentAnalisys(tweets),
        })
    return newsWithTweets

def getGeneralSentmentAnalisys(tweets):
    allTweets = []
    for tweet in tweets:
        allTweets.append(tweet['text'])
    return sentiment_scores_of_array(allTweets)

def getKeywords(text):
    pyake = yake.KeywordExtractor(lan="pt",n=3)

    result = pyake.extract_keywords(text)
    result.sort(key=lambda a: a[1])
    result = [word[0] for word in result]
    keywords = ""
    for word in result[:1]:
        keywords = keywords + word + " "
    return keywords
    

def getTweets(filter):
    tweets = []
    keywords = getKeywords(filter)
    try:
        response = client.search_recent_tweets(
            f"{keywords} -is:retweet lang:pt",
            max_results = 10,
            tweet_fields = ['author_id','created_at','text','source','lang','geo'],
            user_fields = ['name','username','location','verified'],
            expansions = ['geo.place_id', 'author_id'],
            place_fields = ['country','country_code']
        )
        if response.data == None:
            return tweets
        for index, tweet in enumerate(response.data):
            tweets.append({
                    "author": response[1]['users'][index].name,
                    "text": str(tweet),
                    "sentimentAnalisys": sentiment_scores(str(tweet))
                    })
       
        return tweets   
    except Exception as e:
        print(e)
        return tweets