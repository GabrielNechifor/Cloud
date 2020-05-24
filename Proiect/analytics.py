from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import json

key = "b88fe206f8e14f10875e8bdd594d2085"
endpoint = "https://textanalyticsresource34.cognitiveservices.azure.com/"

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

def sentiment_analysis_example(input_text):
    client = authenticate_client()
    documents = [input_text]
    response = client.analyze_sentiment(documents = documents)[0]
    result = dict()
    result["Document_Sentiment"] = response.sentiment
    overall_scores = dict()
    overall_scores["positive"] = response.confidence_scores.positive
    overall_scores["negative"] = response.confidence_scores.negative
    overall_scores["neutral"] = response.confidence_scores.neutral
    result["Overall_scores"] = overall_scores
    result["Sentences"] = []
    for idx, sentence in enumerate(response.sentences):
        tmpsentence = dict()
        tmpsentence["Length"] = sentence.grapheme_length
        tmpsentence["SentenceId"] = idx+1
        tmpsentence["Sentiment"] = sentence.sentiment
        tmpsentence["Positive_score"] = sentence.confidence_scores.positive
        tmpsentence["Negative_score"] = sentence.confidence_scores.negative
        tmpsentence["Neutral_score"] = sentence.confidence_scores.neutral
        result["Sentences"].append(tmpsentence)
    
    return [result]


def language_detection_example(input_text):
    client = authenticate_client()
    try:
        documents = [input_text]
        response = client.detect_language(documents = documents, country_hint = 'us')[0]
        result = dict()
        result["Language"] = response.primary_language.name

    except Exception as err:
        print("Encountered exception. {}".format(err))
    
    return [result]


def entity_recognition_example(input_text):
    client = authenticate_client()
    try:
        documents = [input_text]
        response = client.recognize_entities(documents = documents)[0]
        result = dict()
        result["Entities"] = []
        for entity in response.entities:
            tmpentity = dict()
            tmpentity["Text"] = entity.text
            tmpentity["Category"] = entity.category
            tmpentity["SubCategory"] = entity.subcategory
            tmpentity["Length"] = entity.grapheme_length
            tmpentity["Confidence_Score"] =  round(entity.confidence_score, 2)
            result["Entities"].append(tmpentity)
         
    except Exception as err:
        print("Encountered exception. {}".format(err))
    
    return [result]



def entity_linking_example(input_text):
    
    client = authenticate_client()
    try:
        documents = [input_text]
        response = client.recognize_linked_entities(documents = documents)[0]
        result = dict()
        result["Entities"] = []
        for entity in response.entities:
            tmpentity = dict()
            tmpentity["Name"] = entity.name
            tmpentity["Id"] = entity.data_source_entity_id
            tmpentity["Url"] = entity.url
            tmpentity["Data_Source"] = entity.data_source
            tmpentity["Matches"] = []
            for match in entity.matches:
                tmpmatch = dict()
                tmpmatch["Text"] = match.text
                tmpmatch["Confidence_Score"] = match.confidence_score
                tmpmatch["Length"] = match.grapheme_length
                tmpentity["Matches"].append(tmpmatch)
            result["Entities"].append(tmpentity)
            
    except Exception as err:
        print("Encountered exception. {}".format(err))
    
    return [result]



def key_phrase_extraction_example(input_text):
    
    client = authenticate_client()
    try:
        documents = [input_text]

        response = client.extract_key_phrases(documents = documents)[0]
        result = dict()
        if not response.is_error:
            result["Key_Phrases"] = []
            for phrase in response.key_phrases:
                result["Key_Phrases"].append(phrase)
        else:
            print(response.id, response.error)

    except Exception as err:
        print("Encountered exception. {}".format(err))
    
    return [result]


#print(sentiment_analysis_example("I had the best day of my life. I wish you were there with me."))

#print(entity_linking_example("Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800. During his career at Microsoft, Gates held the positions of chairman,chief executive officer, president and chief software architect, while also being the largest individual shareholder until May 2014."))

#print(language_detection_example("Salut, acest document este in limba mea natala."))
#print(entity_recognition_example("I had a wonderful trip to Seattle last week."))

#print(key_phrase_extraction_example("My cat might need to see a veterinarian."))

