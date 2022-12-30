# import SentimentIntensityAnalyzer class
# from vaderSentiment.vaderSentiment module.
from leia import SentimentIntensityAnalyzer 

# function to print sentiments
# of the sentence.
def sentiment_scores(sentence):

	sid_obj = SentimentIntensityAnalyzer()
	sentiment_dict = sid_obj.polarity_scores(sentence)
	
	if sentiment_dict['compound'] >= 0.05 :
		return "Positivo"

	elif sentiment_dict['compound'] <= - 0.05 :
		return "Negativo"

	else :
		return "Neutro"

def sentiment_scores_of_array(array):

	sid_obj = SentimentIntensityAnalyzer()

	sentiment_dict = sid_obj.polarity_scores_in_array(array)

	if sentiment_dict['compound'] >= 0.05 :
		return "Positivo"

	elif sentiment_dict['compound'] <= - 0.05 :
		return "Negativo"

	else :
		return "Neutro"

