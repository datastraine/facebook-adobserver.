import pandas as pd
import numpy as np
import unicodedata
import re
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split

def basic_clean(somestring):
    '''
    Takes in body text of a README and performs a basic clean by first converting it to all lower case letters,
    then normalizes the encoding, and removes any character that isn't a letter, number, or a space.
    Returns the result.
    '''
    basic = somestring.lower()
    basic = unicodedata.normalize('NFKD', basic).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    basic = re.sub(r"[^a-z0-9'\s]", '', basic)
    return basic

def tokenize(somestring):
    '''
    Creates a tokenizer object to tokenize the given string and then returns the tokenized string
    '''
    tokenizer = nltk.tokenize.ToktokTokenizer()
    tokened = tokenizer.tokenize(somestring, return_str=True)    
    return tokened

def lemmatize(somestring):
    '''
    Creates a lemmatize object and then uses it to lemmatize the provided string. Returns the lemmatized string 
    '''
    wnl = nltk.stem.WordNetLemmatizer()
    lemmas = [wnl.lemmatize(word) for word in somestring.split()]
    article_lemmatized = ' '.join(lemmas)
    return article_lemmatized

def remove_stopwords(string, keep_words=['no', 'not'], exclude_words=[]):
    '''
    This function takes in a string, removes stop_words from the string, and then returns the results.
    The fuction also allows for optional arugments keep_words and exclud_words to modify the stop word list
    * keep_words - a list of words to remove from the standard english stopwords list from nltk.corpus i.e. no or not
    * exclude_words - a list of words to add to the standard english stopwords list from nltk.corpus 
    i.e. ['data', 'science'] to the remove both words when dealing with articles only about data science
    * By default, keep_words includes no and not
    '''
    # Create stopword_list.
    stopword_list = stopwords.words('english')
    # Remove 'keep_words' from stopword_list to keep these in my text.
    stopword_list = set(stopword_list) - set(keep_words)
    # Add in 'exclude_words' to stopword_list.
    stopword_list = stopword_list.union(set(exclude_words))
    # Split words in string.
    words = string.split()
    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]
    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = ' '.join(filtered_words)
    return string_without_stopwords

def wrangle(facebook_data_csv_location):
    '''
    This function requires that you download and unzip the file from the link below. File size is over 3gigs
    https://www.propublica.org/datastore/dataset/political-advertisements-from-facebook 
    Once unzipped, use the file path in the fuction to:
    * Load the csv into a pandas dataframe
    * Drops the following columns - 'listbuilding_fundraising_proba', 'targetedness', 'targetings', 'targets', 
    'targeting', 'images', 'lang', 'thumbnail', 'html', 'page_id', 'suppressed', 'entities', 'lower_page', 'id', and 'political_probability'
    * Create a socio_political_fb column that is 'Political' if facebook believes that the ad is about soical or political topics (advert_by is not null), 
    and 'Not Political' if facebook does not (advert_by is null)
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
    * Creates message and full_ad lengths columns by counting the length of a list created using .str.split() to create a list of words
    * Creates a political_score column by subtracting political from not_political. Negative rating happens when users said 
    an ad was not_political more than political and the opposite for positive numbres
    * returns train, validate, test
    '''
    # read the data in a df
    df = pd.read_csv(facebook_data_csv_location)
    # drops unnecessary colunms
    df.drop(columns=['listbuilding_fundraising_proba', 'targetedness', 'targetings', 'targets', 
    'targeting', 'images', 'lang', 'thumbnail', 'html', 'page_id', 'suppressed', 'entities', 'lower_page', 'id', 'political_probability'], inplace=True)
    # creates the  socio_political_fb column
    df['socio_political_fb'] = df['paid_for_by'].notnull()
    df['socio_political_fb'] = df['socio_political_fb'].replace({True:'Political', False:'Not Political'})
    # combines the paid_for_by and advertized by columns into a advert_by column
    df['advert_by'] = np.where(df.paid_for_by.isnull(), df.advertiser, df.paid_for_by)
    df.advert_by = np.where(df.advert_by.isnull(), df.page, df.advert_by)
    df['advert_by'].fillna('unk', inplace=True)
    # Drops any row where title is null
    df.dropna(subset=['title'], inplace= True)
    # Drops remaining columns with null values 
    df.dropna(axis=1, inplace=True)
    # Removes html font formatting and cleans the message and title texts
    df['message'] = df['message'].str.replace(r'(<.+\")', "")
    df['message'] = df['message'].str.replace("</span>", "")
    df['message'] = df['message'].str.replace("</p>", "")
    df['message'] = df['message'].str.replace("<p>", "")
    df['message'] = df['message'].apply(basic_clean).apply(tokenize).apply(remove_stopwords).apply(lemmatize)
    df['title'] = df['title'].apply(basic_clean).apply(tokenize).apply(remove_stopwords).apply(lemmatize)
    # converts the created_at and updated_at columns to datatime objs
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    # creates a known_ad_time column and adds 1 to results to account for 0 day
    df['known_ad_time'] = df['updated_at'] - df['created_at'] 
    df['known_ad_time'] = df['known_ad_time'] // pd.Timedelta('1d') 
    df['known_ad_time'] = df['known_ad_time'] + 1
    # creates a message length column that is the total number of words of the ad's message
    df['message_length'] = df['message'].str.split().str.len()
    # creates a full_ad column that combines the words from the title and the ad message into a single column
    df['full_ad'] = df['message'] + " " + df['title']
    # creates a full_ad_length that counts the number of words in the full_ad
    df['full_ad_length'] = df['full_ad'].str.split().str.len()
    df['political_score'] = df['political'] - df['not_political']
    # splits the data into train, validate, test sets and stratifies on socio_political_fb
    train_validate, test = train_test_split(df, 
                                        stratify=df.socio_political_fb, 
                                        test_size=.2, 
                                        random_state=333)

    train, validate = train_test_split(train_validate, 
                                       stratify=train_validate.socio_political_fb, 
                                       test_size=.25,
                                       random_state=333)
    return train, validate, test


