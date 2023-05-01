from joblib import load
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0
import numpy as np
import re
import nltk
import pickle
from nltk.corpus import stopwords
from sklearn.datasets import load_files
from sklearn.model_selection import GridSearchCV
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline


class Modelo:
    def __init__(self):
        self.model = load("ModeloFinal.joblib")
        
        
    def predict(self, desc):
        
        df = pd.read_csv('Df_limpio.csv', encoding = "utf8", sep = ",")
        
        df.drop("Unnamed: 0", inplace=True, axis=1)
        
        df.loc[len(df.index)] = [desc, "positivo",20,"es"]
        
        documents = []
        
        stemmer = WordNetLemmatizer()
        
        for i in range(0, len(df)):
            # Remove all the special characters
            document = re.sub(r'\W', ' ', str(df.iloc[i,0]))
            
            # remove all single characters
            document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)
            
            # Remove single characters from the start
            document = re.sub(r'\^[a-zA-Z]\s+', ' ', document) 
            
            # Substituting multiple spaces with single space
            document = re.sub(r'\s+', ' ', document, flags=re.I)
            
            # Removing prefixed 'b'
            document = re.sub(r'^b\s+', '', document)
            
            # Converting to Lowercase
            document = document.lower()
            
            # Lemmatization
            document = document.split()
        
            document = [stemmer.lemmatize(word) for word in document]
            document = ' '.join(document)
            
            documents.append(document)
            
        vectorizer = CountVectorizer(max_features=18000, min_df=5, max_df=0.7, stop_words=stopwords.words('spanish'))
        #X = vectorizer.fit_transform(documents).toarray()
        
        
        tfidfconverter = TfidfTransformer()
        #X = tfidfconverter.fit_transform(X).toarray()
        
        steps = [("vect", vectorizer),("tfid", tfidfconverter)]
        pipeline = Pipeline(steps)
        
        X = pipeline.fit_transform(documents)
        
        return self.model.predict(X)[-1]
        
        
prueba = Modelo()

print(prueba.predict("Me encanta esta pelicula"))
        
        
        

        
        