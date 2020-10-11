import nltk
import json
import spacy
import random
import pytextrank
import psycopg2
import numpy as np
import pandas as pd

from newsapi.newsapi_client import NewsApiClient
from rake_nltk import Rake
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

global connection

config = None
with open('config.json') as f:
    config = json.load(f)


def get_news_data(_category='general', _language='en', _country='us', _pagesize=100, _page=1):
    # set api key
    newsapi = NewsApiClient(api_key=config["news_api_key"])

    # get news data from the news api
    top_headlines = newsapi.get_top_headlines(
        category=_category,
        language=_language,
        country=_country,
        page_size=_pagesize,
        page=_page
    )
    return top_headlines


def parse_news_data(top_headlines):
    articles = raw_news_list['articles']
    df = pd.DataFrame(articles)
    df = df.dropna(subset=['source', 'title',
                        'description', 'url', 'urlToImage', 'content'])
    df = df[df['description'] != ''].reset_index(drop=True)
    df['source'] = [source['name'] for source in df['source']]

    # Remove source name in title
    df['title'] = [df.loc[title_row,
                        'title'][:df.loc[title_row, 'title'].rfind('-')-1] for title_row in range(len(df))]
    # Remove the endig of the content column
    df['content'] = [df.loc[content_row,
                            'content'][:df.loc[content_row, 'content'].rfind('[')-1] for content_row in range(len(df))]
    # Process author column
    removelist = [', CNN Business', ' | The Oregonian/OregonLive', ', CNN', ' | NJ Advance Media for NJ.com', ' | NJ Advance Media For NJ.com',
                'WGN-TV', 'By ', ' For Dailymail.com', ' For Daily Mail Australia', 'Associated Press', ' | For lehighvalleylive.com', ' (NEWS CENTER Maine)']
    for author_row in range(len(df)):
        author, source = df.loc[author_row, 'author'], df.loc[author_row, 'source']
        # remove author if author name is the same as source name or if it contains staff
        df.loc[author_row, 'author'] = None if source == author else author
        if 'Staff' in str(author) or 'staff' in str(author):
            df.loc[author_row, 'author'] = None
        # remove redundant words
        for r in removelist:
            df.loc[author_row, 'author'] = author.replace(
                r, '') if r in str(author) else df.loc[author_row, 'author']

    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    for textrow in range(len(df)):
        title_text, desc_text = df['title'][textrow], df['description'][textrow]
        title_doc = nlp(title_text)
        title_phraselist = [str(p) for p in title_doc._.phrases]

    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

    for textrow in range(len(df)):
        title_text, desc_text = df['title'][textrow], df['description'][textrow]
        title_doc = nlp(title_text)
        title_phraselist = [str(p) for p in title_doc._.phrases]
        if len(title_phraselist) < 3:
            r = Rake()
            r.extract_keywords_from_text(title_text)
            rakekeywords = r.get_ranked_phrases()
            title_phraselist += rakekeywords
        tag1 = tag2 = tag3 = None
        if isinstance(desc_text, type(None)) is False:  # if desc is not empty
            desc_doc = nlp(desc_text)
            desc_phraselist = [str(p) for p in desc_doc._.phrases]
            # compare the keywords from title and description and assign the more significant one
            if len(set(title_phraselist) & set(desc_phraselist)) == 1:
                tag1 = list(set(title_phraselist) & set(desc_phraselist))[0]
                title_phraselist.remove(tag1)
                tag2 = title_phraselist[0] if len(
                    title_phraselist) > 0 else None
                tag3 = title_phraselist[1] if len(
                    title_phraselist) > 1 else None

            elif len(set(title_phraselist) & set(desc_phraselist)) == 2:
                tag1, tag2 = list(set(title_phraselist) & set(desc_phraselist))[
                    0], list(set(title_phraselist) & set(desc_phraselist))[1]
                title_phraselist.remove(tag1)
                title_phraselist.remove(tag2)
                tag3 = title_phraselist[0] if len(
                    title_phraselist) > 0 else None

            elif len(set(title_phraselist) & set(desc_phraselist)) == 3:
                tag1, tag2, tag3 = list(set(title_phraselist) & set(desc_phraselist))[0], list(set(
                    title_phraselist) & set(desc_phraselist))[1], list(set(title_phraselist) & set(desc_phraselist))[2]

            else:  # not even one overlapped
                tag1 = title_phraselist[0] if len(
                    title_phraselist) > 0 else None
                tag2 = title_phraselist[1] if len(
                    title_phraselist) > 1 else None
                tag3 = title_phraselist[2] if len(
                    title_phraselist) > 2 else None

            df.loc[textrow, 'tag1'], df.loc[textrow,
                                            'tag2'], df.loc[textrow, 'tag3'] = tag1, tag2, tag3
        else:
            tag1 = title_phraselist[0] if len(title_phraselist) > 0 else None
            tag2 = title_phraselist[1] if len(title_phraselist) > 1 else None
            tag3 = title_phraselist[2] if len(title_phraselist) > 2 else None
            df.loc[textrow, 'tag1'], df.loc[textrow,
                                            'tag2'], df.loc[textrow, 'tag3'] = tag1, tag2, tag3
    # Start keyword matching between article pair
    # Remove stop words to avoid meaningless keywords matching
    stop_words = set(stopwords.words('english')) 

    for col in ['tag1','tag2','tag3']:
        df[col]= df[col].fillna('none')

    for col in ['tag1','tag2','tag3']:
        for row in range(len(df)):
    #         print(df.loc[row,col])
            df.loc[row,col] = [w for w in word_tokenize(df.loc[row,col])  if not w in stop_words] 
    #         print(row,col)

    df['tags'] = df['tag1']+df['tag2']+df['tag3']


    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3

    # Find the related articles by checking if there are overlapped tags
    related_list = []
    for row in range(len(df)):
        related_comparerows = []
        for compare_row in range(len(df)):
            if compare_row != row:
                if len(intersection(df.loc[row, 'tags'], df.loc[compare_row, 'tags'])) > 0:
                    related_comparerows.append(compare_row)
        related_list.append(related_comparerows)

    # Randomly choose one related article if no overlapped tags
    for num in range(len(related_list)):
        if len(related_list[num]) == 0:
            choosing_range = list(range(1, num)) + \
                list(range(num+1, len(related_list)))
            related_list[num] += random.sample(choosing_range, 1)
        if len(related_list[num]) > 5:
            choosing_range = list(range(1, num)) + \
                list(range(num+1, len(related_list)))
            related_list[num] = random.sample(choosing_range, 5)
    df['related_num'] = related_list

    # drop the unneeded columns
    df = df.drop(['tag1', 'tag2', 'tag3', 'tags',
                'related_num', 'description'], axis=1)
    # create relative dictionaries
    df['records'] = df.drop(
        ['content', 'urlToImage', 'author'], axis=1).to_dict('records')
    total_relative_list = []
    for art_num in range(len(df)):
        current_relative_list = [df.loc[rel, 'records']
                                for rel in related_list[art_num]]
        total_relative_list.append(current_relative_list)
    df['related_articles'] = total_relative_list
    df = df.drop(['records'], axis=1)

    parsed_news_list = df.to_dict('records')
    return(parsed_news_list)


# def parse_news_data(top_headlines):
    articles = top_headlines['articles']
    df = pd.DataFrame(articles)
    df = df.dropna(subset=['source', 'title',
                           'description', 'url', 'urlToImage', 'content'])
    df = df[df['description'] != ''].reset_index(drop=True)
    df['source'] = [source['name'] for source in df['source']]

    # Remove source name in title
    df['title'] = [df.loc[title_row,
                          'title'][:df.loc[title_row, 'title'].rfind('-')-1] for title_row in range(len(df))]
    # Remove the endig of the content column
    df['content'] = [df.loc[content_row,
                            'content'][:df.loc[content_row, 'content'].rfind('[')-1] for content_row in range(len(df))]
    # Process author column
    removelist = [', CNN Business', ' | The Oregonian/OregonLive', ', CNN', ' | NJ Advance Media for NJ.com', ' | NJ Advance Media For NJ.com',
                  'WGN-TV', 'By ', ' For Dailymail.com', ' For Daily Mail Australia', 'Associated Press', ' | For lehighvalleylive.com', ' (NEWS CENTER Maine)']
    for author_row in range(len(df)):
        author, source = df.loc[author_row,
                                'author'], df.loc[author_row, 'source']
        # remove author if author name is the same as source name or if it contains staff
        df.loc[author_row, 'author'] = None if source == author else author
        if 'Staff' in str(author) or 'staff' in str(author):
            df.loc[author_row, 'author'] = None
        # remove redundant words
        for r in removelist:
            df.loc[author_row, 'author'] = author.replace(
                r, '') if r in str(author) else df.loc[author_row, 'author']

    # load a spaCy model, depending on language, scale, etc.
    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    tr = pytextrank.TextRank()
    nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
    for textrow in range(len(df)):
        title_text, desc_text = df['title'][textrow], df['description'][textrow]
        title_doc = nlp(title_text)
        title_phraselist = [str(p) for p in title_doc._.phrases]
        tag1 = tag2 = tag3 = None
        if isinstance(desc_text, type(None)) is False:  # if desc is not empty
            desc_doc = nlp(desc_text)
            desc_phraselist = [str(p) for p in desc_doc._.phrases]
            # compare the keywords from title and description and assign the more significant one
            if len(set(title_phraselist) & set(desc_phraselist)) == 1:
                tag1 = list(set(title_phraselist) & set(desc_phraselist))[0]
                title_phraselist.remove(tag1)
                tag2 = title_phraselist[0] if len(
                    title_phraselist) > 0 else None
                tag3 = title_phraselist[1] if len(
                    title_phraselist) > 1 else None

            elif len(set(title_phraselist) & set(desc_phraselist)) == 2:
                tag1, tag2 = list(set(title_phraselist) & set(desc_phraselist))[
                    0], list(set(title_phraselist) & set(desc_phraselist))[1]
                title_phraselist.remove(tag1)
                title_phraselist.remove(tag2)
                tag3 = title_phraselist[0] if len(
                    title_phraselist) > 0 else None

            elif len(set(title_phraselist) & set(desc_phraselist)) == 3:
                tag1, tag2, tag3 = list(set(title_phraselist) & set(desc_phraselist))[0], list(set(
                    title_phraselist) & set(desc_phraselist))[1], list(set(title_phraselist) & set(desc_phraselist))[2]

            else:  # not even one overlapped
                tag1 = title_phraselist[0] if len(
                    title_phraselist) > 0 else None
                tag2 = title_phraselist[1] if len(
                    title_phraselist) > 1 else None
                tag3 = title_phraselist[2] if len(
                    title_phraselist) > 2 else None

            df.loc[textrow, 'tag1'], df.loc[textrow,
                                            'tag2'], df.loc[textrow, 'tag3'] = tag1, tag2, tag3
        else:
            tag1 = title_phraselist[0] if len(title_phraselist) > 0 else None
            tag2 = title_phraselist[1] if len(title_phraselist) > 1 else None
            tag3 = title_phraselist[2] if len(title_phraselist) > 2 else None
            df.loc[textrow, 'tag1'], df.loc[textrow,
                                            'tag2'], df.loc[textrow, 'tag3'] = tag1, tag2, tag3

    tags_list = [df.loc[row, ['tag1', 'tag2', 'tag3']].tolist()
                 for row in range(len(df))]
    df['tags'] = tags_list

    def intersection(lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3
    # Find the related articles by checking if there are overlapped tags
    related_list = []
    for row in range(len(df)):
        related_comparerows = []
        for compare_row in range(len(df)):
            if compare_row != row:
                if len(intersection(df.loc[row, 'tags'], df.loc[compare_row, 'tags'])) > 0:
                    related_comparerows.append(compare_row)
        related_list.append(related_comparerows)
    # Randomly choose related articles if no enough overlapped tags
    for r in related_list:
        if len(r) == 0:
            r += random.sample(range(0, len(df)), 3)
        elif len(r) == 1:
            r += random.sample(range(0, len(df)), 2)
        elif len(r) == 2:
            r += random.sample(range(0, len(df)), 1)
        else:
            r = r[:3]

    df['related_num'] = related_list
    # drop the unneeded columns
    df = df.drop(['tag1', 'tag2', 'tag3', 'tags',
                  'related_num', 'description'], axis=1)
    # create relative dictionaries
    df['records'] = df.drop(
        ['content', 'urlToImage', 'author'], axis=1).to_dict('records')
    total_relative_list = []
    for art_num in range(len(df)):
        current_relative_list = [df.loc[rel, 'records']
                                 for rel in related_list[art_num]]
        total_relative_list.append(current_relative_list)
    df['related_articles'] = total_relative_list
    df = df.drop(['records'], axis=1)

    parsed_news_list = df.to_dict('records')
    return(parsed_news_list)


def insert_parsed_news_to_database(_parsed_news_list, _category):
    """ Connect to the PostgreSQL database server """
    connection = None

    try:
        # connect to the PostgreSQL server @ Azure
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(user=config["azure_db_user"],
                                      password=config["azure_db_password"],
                                      host=config["azure_db_host"],
                                      port=config["azure_db_port"],
                                      database=config["azure_db_database"])

        # create a cursor
        cursor = connection.cursor()

        # execute a statement
        postgres_insert_query = """ INSERT INTO public.Articles (source, author, title, url, url_Image, published_date, category, related_articles, content) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        record_to_insert = []
        for i in range(len(_parsed_news_list)):
            if _parsed_news_list[i]['title'] == None:
                continue
            record_to_insert.append((_parsed_news_list[i]['source'],
                                     _parsed_news_list[i]['author'],
                                     _parsed_news_list[i]['title'],
                                     _parsed_news_list[i]['url'],
                                     _parsed_news_list[i]['urlToImage'],
                                     _parsed_news_list[i]['publishedAt'],
                                     _category,
                                     json.dumps(
                                         _parsed_news_list[i]['related_articles']),
                                     _parsed_news_list[i]['content']))
        cursor.executemany(postgres_insert_query, record_to_insert)
        connection.commit()
        print('Inserted [{}] news successfully'.format(_category))

        # close the communication with the PostgreSQL
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')


def delete_all_record():
    connection = None
    try:
        # connect to the PostgreSQL server @ Azure
        print('Connecting to the PostgreSQL database...')
        connection = psycopg2.connect(user=config["azure_db_user"],
                                      password=config["azure_db_password"],
                                      host=config["azure_db_host"],
                                      port=config["azure_db_port"],
                                      database=config["azure_db_database"])

        # create a cursor
        cursor = connection.cursor()

        # execute a statement
        postgres_delete_query = """ DELETE from public.Articles """
        cursor.execute(postgres_delete_query)
        connection.commit()
        print("All of records deleted successfully ")

        # close the communication with the PostgreSQL
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if connection is not None:
            connection.close()
            print('Database connection closed.')


delete_all_record()

categories = ["general", "business", "entertainment",
              "health", "science", "sports", "technology"]

for i in range(0, 7):
    my_category = categories[i]
    raw_news_list = get_news_data(_category=my_category)
    parsed_news_list = parse_news_data(raw_news_list)
    insert_parsed_news_to_database(parsed_news_list, _category=my_category)
