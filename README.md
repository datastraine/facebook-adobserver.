## Predict the Code - An NLP Project**
## Table of Contents
- [Goal](#goal)
- [Wrangle](#wrangle)
- [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
  - [Visualizations](#visualizations)
  - [Hypothesis Testing & Feature Selection](#hypothesis-testing--feature-selection)
- [Modeling](#modeling)
- [Results & Conclusion](#results--conclusion)
  - [Recommendations](#recommendations)
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

* Loads the csv into a pandas dataframe
* Drops the following columns - 'listbuilding_fundraising_proba', 'targetedness', 'targetings', 'targets', 'targeting', 'images', 'lang', 'thumbnail', 'html', 'page_id', 'suppressed', 'entities', 'lower_page'
* Create a socio_political_fb column that is True if Facebook believes that the ad is about social or political issues, and false if Facebook does not
* Combine the advertiser and paid_for_by columns, with a priority given to paid_for_by values into a advert_by column
* If advert_by column is null and the page is known, replace the null value with the page value
* Fills remaining null values with 'unk' for advert_by column
* Drops any row that has a missing title value (47)
* Drops the paid_for_by, advertiser, and page columns
* Normalizes the message columns by conducting basic_clean, tokenization, removing stop words, and lemmatizing the text
* Returns the cleaned DF

# Exploratory Data Analysis (EDA)
After wrangling the data we conducted EDA on our train data set in order to glean insights from our data. We accomplished this by creating several visualizations that focused on which words are primarily used within our data, using those words to create additional features for our analysis, and then conducting hypothesis testing on the features we created.

## Visualizations


## Hypothesis Testing & Feature Selection

# Modeling

# Results & Conclusion


## Recommendations 


## Next Steps


# Data Dictionary 
| Name | Description |
|---|---|
|   |   |
|   |   |
|   |   |
|   |   |
|   |   |
|   |   |
|   |   |
|   |   |