

# Clean text
# 1. Create a text file and get text from it
# 2. Convert all the letters into lowercase('Apple' is not hte same 'apple)
# 3. Remove punctuations
import matplotlib
import streamlit as st
import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
import GetOldTweets3 as got
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer 


st.title("Twitter and Text analysis")


def process_text(text):
    lower_case=text.lower()
                
    cleaned_text = lower_case.translate(str.maketrans('','',string.punctuation))
   
    tokenized_words= word_tokenize(cleaned_text,"english")
    
    final_words=[]
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)
            
    emotion_list = []
    emotion_string=""
    with open(r"emotions.txt","r") as file:
        for line in file:
            clear_line = line.replace('\n','').replace(',','').replace("'","").strip()
            word, emotion = clear_line.split(':') 
                        
            if word in final_words:
                emotion_list.append(emotion)
                emotion_string+=" "
                emotion_string+=emotion
                
                
    w = Counter(emotion_list)
    if len(emotion_list)!=0:
        score = SentimentIntensityAnalyzer().polarity_scores(emotion_string)
        neg = score['neg']
        
        pos=score['pos']
        if neg>pos :
            st.write("Negative Sentiment")
        elif pos>neg:
            st.write("Positive Sentiment")
        else:
            st.write("Neutral vibe")
        plt.bar(w.keys(),w.values())
                    
        #One or more graphs can be created in figures.
        #The Axes is what we think of a 'a plot'. A given figure can contain many Axes, but a given Axes object can only be in one Figure. 
        fig, axl = plt.subplots()
        axl.bar(w.keys(),w.values())
        fig.autofmt_xdate()
        plt.savefig('graph.png')
        
        st.pyplot()
      
        
    else:
        st.info("Sorry, no emotion found in your text")

def get_tweets():
    print(start_Time)
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query)\
                                           .setSince(start_Time)\
                                           .setUntil(end_Time)\
                                           .setMaxTweets(no_of_tweets)
    #List of objects gets stored in tweets variable
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    #Iterating through tweets, and storing the strings as a list in a list
    text_tweets = [[tweet.text] for tweet in tweets]
    
    
    return text_tweets

choice=st.selectbox("Which analysis do you want to perform?",["Text Analysis","Twitter analysis"])
if choice=="Text Analysis":
    text=st.text_area("Enter your text here","Type here...")
    #Converting text to lower case
    if st.button("Enter"):
        
        if len(text)!=0:
            with st.spinner("Please wait while we process your text"):
                process_text(text)
               
        else:
            st.warning("Please enter some text")
else:
    query=st.text_input("Enter your search query","Twitter")
    startTime=st.date_input("Enter the date from which you want your analysis to start")
    endTime=st.date_input("Enter the ending date till which you want to search")
    No_of_tweets=st.text_input("Enter the no. of tweets you want to search", "50")
    
    
    start_Time=startTime.strftime('%Y-%m-%d')
    end_Time=endTime.strftime('%Y-%m-%d')
    if st.button("Enter"):
        
        if(len(query)!=0 and len(No_of_tweets)!=0 and No_of_tweets.isnumeric()==True):
            no_of_tweets=int(No_of_tweets)
            with st.spinner('Please wait while we get you the graph'):
                tweets=get_tweets()
            if len(tweets) == 0:
                st.info("Sorry no tweets available. Either try to change the query or the time period")
            else:          
                num_of_tweets=len(tweets)
                text=""
                for i in range(0,num_of_tweets):
                    text = tweets[i][0] + " " + text
                
                print(text)
                
                process_text(text)
        else:
            if len(query)==0:
                st.warning("Please enter a query")
            elif len(No_of_tweets)==0:
                st.warning("Please enter the number of tweets")
            elif No_of_tweets.isnumeric()==False:
                st.warning("Please enter a number as number of tweets")
            else:
                st.warning("Please enter the query and the number of tweets")
