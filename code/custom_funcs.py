#!/usr/bin/env python3

import re
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer


class Tfidf_BigramReducer(BaseEstimator, TransformerMixin):
    """
    A class that wraps around sklearn's TfidfVectorizer with ngram_range=(1,2), and subsequently slices out the bigrams with low overall importance

    Attributes
    ----------
    bf (float or int) : 
        the 'bigram fraction' to be kept. If int, an absolute number. If float, a fraction of the total nr of bigrams
    inds_to_keep (list):
        the column indexes to keep in the vectorized matrix. Calculated when the fit method is called 
    all the TfidfVectorizer hyperparameters: 
        these are passed straight through to a TfidfVectorizer object, which is created when this class is instantiated

    Methods
    -------
    fit(X, y=None):
        Fits and transforms input data with TfidfVectorizer,then finds the bigrams with highest summed tfidfvalue over all rows. Calculates which column indices should be kept
    transform(X, y=None):
        transformed the data TfidfVectorizer, then uses the inds_to_keep attribute to slice out all the bigrams with low tfidf value
    get_feature_names_out(X):
        returns the feature names after slicing out bigrams

    inherits methods from Transformer Mixin (fit_transform) and BaseEstimator
    """
    def __init__(self, bf=0.9, stop_words=None, strip_accents=None, max_features=None, tokenizer=None, min_df=1, max_df=0.8, preprocessor=None):
        """
        Constructs the 'bigram frequency' attribute, and creates a TfidfVectorizer object with all the hyperparameters passed through
        """
        self.bf = bf
        
        #tfidf hyperpars
        self.max_df = max_df
        self.min_df = min_df
        self.preprocessor=preprocessor
        self.stop_words = stop_words
        self.strip_accents = strip_accents
        self.tokenizer = tokenizer
        self.max_features = max_features
        
        #create TfidfVectorizer object
        self.tfidf = TfidfVectorizer(stop_words=self.stop_words, min_df=self.min_df, max_df=self.max_df, strip_accents=self.strip_accents, \
                            ngram_range=(1,2), max_features=self.max_features, tokenizer=self.tokenizer, preprocessor=self.preprocessor)

    def fit(self, X, y=None):
        """
        Fits the data to TfidfVectorizer, then uses the tfdidf values to obtain the indexes of the columns to keep
        """
        
        X_trans = self.tfidf.fit_transform(X)
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
        """
        Transforms input data by slicing, using the self.inds_to_keep attribute
        """
        X_trans = self.tfidf.transform(X)
        return X_trans[:,self.inds_to_keep]
    
    def get_feature_names_out(self, X):
        """
        Returns feature names after slicing out bigrams. This function call needs this exact name so it works together with the get_feature_names_out() method of ColumnTransformer
        Note that in older versions of sklearn this method was called get_feature_names, in which case this method name needs to be changed
        """
        return self.features[self.inds_to_keep]
        
# Custom preprocessor
def my_preprocessor(text):
    text = text.lower()
    text = re.sub('\\n', '', text)
    text = re.findall("[\w']+|\$[\d\.]+", text)
    text = ' '.join(text)
    
    return text
