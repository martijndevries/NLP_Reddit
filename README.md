# Project 3 - Web APIs and Natural Language Processing with Reddit

by Martijn de Vries </br>
martijndevries91@gmail.com

## Problem Statement

A US political consultancy company is researching how news sources and discussed topics differ between the US political mainstream and the conservative right-wing media. In the last decade or so, the US political right-wing has been increasingly described as living in an entirely separate information ecosystem from the political mainstream. In order to gauge how intense this effect is, we will collect, process, and classify the Reddit content of two politically-themed subreddit that reflect the mainstream and conservative voters respectively: <b>r/politics</b> and <b>r/conservative</b>. 

For this project, we will build two separate branches of models: one for post submissions (largely consisting of links to news sites), and another for comments (consisting of actual Reddit users discussing political news). As this is a binary classification problem where the two classes are of equal interest and will be approximately balanced, we will use the accuracy score as the main metric to gauge the success of the classification model. 

Because political news is always evolving, we have chosen a specific moment in time: the month leading up to the 2022 midterms, October 6th to November 6th 2022. This ensures that 1) the same news cycle is covered for both subreddits, 2) both subreddits were at peak activity, and 3) maximum potential for interesting insights in the way that news is discussed within these two subreddits.

## Repository Overview
    
This repository consists of the following:

<ul>
   <li> The directory <code>./code</code> contains five notebooks that go through each of the steps of the analysis: 
   
   <ol>
    <li> In <b>data_collection.ipynb</b>, I use the Pushshift API to collect the data from reddit, which are then saved to dataframes </li>
    <li> In <b>EDA_and_cleaning.ipynb</b>, I do some cleaning of the dataframes, like deleting duplicates and non-english posts. I also do some EDA related to word frequencies and figure out which features to use in the model </li> 
    <li> In <b>sentiment_analysis.ipynb</b>, I use the roBERTa-based sentiment analysis to obtain sentiment labels and scores for each of the comments in the cleaned dataframe </li>
    <li> In <b>NLP_and_modeling.ipynb</b>, I set up an sklearn pipeline for natural language processing, and try out several different models, and save the best-performing model objects with pickle </li>
    <li> In <b>model_insights_conclusions.ipynb</b>, I do interpretation regarding the most significant features, and give my overall conclusions to the project </li>
    <li><b>custom_funcs.py</b> contains one function and a custom sklearn transformer class that I wrote during the project, so that I could reuse them across different notebooks. </li>
   </ol>
  <li> The directory <code>./data</code> contains dataframes with the collected data from reddit for both post titles and comments, as well as cleaned versions of these dataframes. Additionally, for the comments data there is an extra .csv file which appends the sentiment analysis features to the cleaned comments dataframe.
    <li> The directory <code>./pickled_models/</code> is to save the pickled model objects that are saved in the NLP and modeling notebook. These were not uploaded to the remote repository for storage space reasons, so they will have to be recreated in the notebook.
   <li> The directory <code>./figures</code> contains all the figures that are saved during the analysis in the notebooks, in .png formats </li>
    <li> The slides for the project presentation are in the file <code>project3_martijn_slides.pdf</code> </li>
</ul>

## Data Dictionary: Posts

|Feature|Type|Dataset|Description|
|---|---|---|---|
|Title | string | Reddit | The title of the subreddit post. Typically the headline of a news article
|num_comments| int | Reddit | the number of comments below each post 
|domain| int | Extracted from pushshift | 
|Subreddit| category | Pushshift| ***Target variable***- The subreddit the post is from: r/conservative or r/politics

