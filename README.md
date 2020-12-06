## Predict the Code - An NLP Project**
## Table of Contents
- [Goal](#goal)
- [Wrangle](#wrangle)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
  - [Hypothesis Testing](#hypothesis-testing)
- [Modeling](#modeling)
- [Results & Conclusion](#results--conclusion)
  - [Next Steps](#next-steps)
- [Data Dictionary](#data-dictionary)

# Goal
The goal of this project is to predict if an ad posted on Facebook is political or not using Natural Language Processing and other metrics. The data I used for this project came from the [Political Advertisements from Facebook](https://www.propublica.org/datastore/dataset/political-advertisements-from-facebook). The data was collected from 1000s of people, all around the world, who installed a web browser extension called AdObserver. The data contains over 200k individual ads from the year 2020. You can read more about AdObserver and it's goals at [NYU's Online Political Transparency Project](https://onlinepoliticaltransparencyproject.org/).

**Note** - To reproduce this project you must download and extract the CSV yourself

I will deliver the following:
  * A [wrangle.py]() module that prepares the data for analysis
  * A [Final Project notebook]() that details every step of this project.
  * A 5-minute presentation about the project, including slides.
  * A [Data Dictionary](#data-dictionary) for data used in this project.
  
# Wrangle
The wrangle function takes in the [Political Advertisements from Facebook](https://www.propublica.org/datastore/dataset/political-advertisements-from-facebook) data (as a CSV) and does the following:

* Load the csv into a pandas dataframe
* Drops the following columns - 'listbuilding_fundraising_proba', 'targetedness', 'targetings', 'targets', 'targeting', 'images', 'lang', 'thumbnail', 'html', 'page_id', 'suppressed', 'entities', 'lower_page', 'id', and 'political_probability'
* Create a socio_political_fb column that is 'Political' if Facebook believes that the ad is about social or political topics (advert_by is not null), 
and 'Not Political' if Facebook does not (advert_by is null)
* Combine the advertiser and paid_for_by columns, with a priority given to paid_for_by values into a advert_by column
* If advert_by column is null and the page is known, replace the null value with the page value
* Fills remaining null values with 'unk' for advert_by column
* Drops any row that has a missing title value (47)
* Drops the remaining columns with null 
* Normalizes the message and title columns by conducting basic_clean, tokenization, removing stop words, and lemmatizing the text
* Transforms 
* Creates a known_ad_time column which is when the ad was last updated minus when the ad was first seen
* Combines the message and title columns into a full_ad column 
* Creates a known_ad_time column that is the difference between the updated_at and created_at, and adds 1 to result to account for 0 day
* Splits the data into train, validate, and test sets that are stratified on socio_political_fb
* Creates a political_score column by subtracting political from not_political. Negative rating happens when users said an ad was not_political more than political and the opposite for positive numbers
* Returns the train, validate, test data sets

# Exploratory Data Analysis (EDA)
After wrangling the data we conducted EDA on our train data set in order to glean insights from our data. We accomplished this by creating several visualizations that focused on which words are primarily used within our data, and several scatter plots of our continuous features. From these visualizations, we discovered we may want to add the following words to our stopword list.

> need', 'help', 'trump', 'today', 'make', 'right', and people

Additionally we identified impressions, full_ad_length, and known_ad_time as possible feature to use in our model.

## Hypothesis Testing

For hypothesis testing we conducted Two Sample; Two Tail T-test on our features and rejected the null hypothesis for each. The hypothesis tests were:

* **Impressions**
  - $H0$ The average impressions of political ads is the same as the average impressions for non-political ads
  - $Ha$ The average impressions of political ads is less than the average impressions for non-political ads

* **Ad Length**
  - $H0$ The average ad length of political ads is the same as the average ad length for non-political ads
  - $Ha$ The average ad length of political ads is not the same as the avg ad length for non-political ads

* **Known Ad Time**
  - $H0$ The average known ad time of political ads is the same as the average known ad time for non-political ads
  - $Ha$ The average known ad time of political ads is not the same as average known ad time for non-political ads


# Modeling
We created 6 models, including the baseline model.  The models are as follows:

* **Baseline** model where every ad is a political ad
* **Model 1** uses bag-of-words on message to create a feature based on  and logistic regression to make predictions
* **Model 2** uses bag-of-words on full ad to create a feature based on and logistic regression to make predictions
* **Model 3** uses tf-idf on message to create a feature and logistic regression to make predictions
* **Model 4** uses tf-idf on full_ad to create a feature and logistic regression to make predictions
* **Model 5** uses ad_length, known_ad_time, and impressions as features in a logistic regression model

We will use F1-score as our evaluation metric. The reason for using F1-score is because we want to correctly identify when an ad is in fact political in nature or not, and thus care equally about both false negatives and false positives results.

# Results & Conclusion
After building our models and validating the ones that performed best on train, we found that Model 2, which used bag-of-words on the full ad feature, showed the most promise. While the model appears to be slightly over-fitted to the train data, it still performed very well on the test data set with a f1-score of 91% for 'political' ads and 72% for 'not political' ads. Based on the current model, I would recommend Facebook, if it isn't already, to create a BoW feature for it's political ad classification system

## Next Steps

While the our BoW on the full ad feature worked really well, there is always room for improvement. For the next iteration(s) of this project I would:

* Remove the following words from the full_ad feature: **need', 'help', 'trump', 'today', 'make', 'right', and people**
* See if AdObserver users political_score has any bearing on whether an ad is political or not
* Attempt to come up with a probability range for each ad whether it is political or not
* Create a contains_candidate feature where true if a political candidate's name is mentioned in full_ad 
* See if combining BoW features with other features improves the model
* See if there are any clusters of features that may identify political ads

# Data Dictionary

| Name | Description |
|---|---|
| message  | The text of the ad's message  |
| title  | The title of the ad  |
| full_ad  | The text of the ad's message and title  |
| political  | The number of times an AdObserver users rated an ad political  |
| not_political  | The number of times an AdObserver users rated an ad non-political  |
| created_at  | The date and time an ad was first seen  |
| updated_at  | The date and time that an ad was last seen  |
| known_ad_time  | The number of days an ad was known to run. Adds a day to account for when the ad was first seen  |
| impressions  | The number of time an ad was seen  |
| political_score  | The difference between a the user raiting of political and not_political  |
| advert_by  | Who published the ad  |
| socio_political_fb | How facebook classifies an ad  |
| message_length  | The number of words contained in an ad's message |
| full_ad_length  |  The number of words contained in an ad's full_ad |
