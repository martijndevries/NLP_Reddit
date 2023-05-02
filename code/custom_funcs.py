#!/usr/bin/env python3

import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer


class Tfidf_BigramReducer(BaseEstimator, TransformerMixin):
    """
    Transformer class that wraps around TfidfVectorizer, and postprocesses the output.
    The idea is to reduce the number of bigrams 
    and only keep the monograms and the 'bf' most frequent bigrams. The other bigrams are sliced out
    """
    def __init__(self, bf=0.9, stop_words=None, strip_accents=None, max_features=None, tokenizer=None, min_df=1, max_df=0.8, preprocessor=None):
        
        #nr of most frequent bigrams to keep. Can either be an int > 1 (absolute nr), or a float =<1 (percentage)
        self.bf = bf 
        
        #tfidf hyperpars
        self.max_df = max_df
        self.min_df = min_df
        self.preprocessor=preprocessor
        self.stop_words = stop_words
        self.strip_accents = strip_accents
        self.tokenizer = tokenizer
        self.max_features = max_features
        
        #instantiate TfidfVectorizer object
        self.tfidf = TfidfVectorizer(stop_words=self.stop_words, min_df=self.min_df, max_df=self.max_df, strip_accents=self.strip_accents, \
                            ngram_range=(1,2), max_features=self.max_features, tokenizer=self.tokenizer, preprocessor=self.preprocessor)

    def fit(self, X, y=None):
        """
        .fit() first calls the TfidfVectorizer instantiated when this object was instantiated. Then finds out which columns to keep 
        and which ones to slice out of the matrix. I'm keeping everything in sparse matrix dtype for efficiency
        """
        
        X_trans = self.tfidf.fit_transform(X)

        #get features from tfidf object
        self.features = self.tfidf.get_feature_names_out()
        
        #Sum over all rows to find most frequently occuring n-grams
        X_q = np.sum(X_trans, axis=0) 
                
        #Isolate the bigrams, sort by size
        mc_bigram_freqs = sorted([X_q[0,x] for x in range(X_q.shape[1]) if len(self.features[x].split(' ')) == 2])

        #Find the summed frequency above which we should keep the bigram (depending on self.bf)
        if type(self.bf) == int:
            cutoff = mc_bigram_freqs[-self.bf]
        elif (type(self.bf) == float) and self.bf <= 1.0:
            idx = int((1-self.bf)*len(mc_bigram_freqs))
            cutoff = mc_bigram_freqs[idx]
        else:
            sys.exit('Bf can only be an integer above 1 or a float below 1')
    
        #Find which col indexes in the matrix to keep (either its a monogram, or a bigram above the cutoff) - save as attribute
        self.inds_to_keep = [x for x,f in enumerate(self.features) if len(f.split(' ')) == 1 or X_q[0,x] >= cutoff]

        return self

    def transform(self, X, y=None):
        X_trans = self.tfidf.transform(X)
        return X_trans[:,self.inds_to_keep]
        
    #Need this function so I know which features are actually fit at the end
    def get_feature_names_out(self, X):
        return self.features[self.inds_to_keep]
        
# Custom preprocessor
def my_preprocessor(text):
    text = text.lower()
    text = re.sub('\\n', '', text)
    text = re.findall("[\w']+|\$[\d\.]+", text)
    text = ' '.join(text)
    
    return text
