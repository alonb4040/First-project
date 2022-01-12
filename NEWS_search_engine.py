
'''

News search engine

Sending customized articles’ details to your Email address.
You can get articles based on keywords for your interest. The engine will search the entire articles’ bank, by titles, based on what’s relevant to your keywords. You can filter the web searches results, by a full match or a partial match and even by a specific date.


*Note - the script is insensitive (doesn't matter if you use upper-case\lower-case letters).


Partial match - searching for articles and sending all the articles that their title contains the sequence of the keyword.
For example: for the keyword 'cov' the engine returns articles which in their title there׳s the sequence 'cov' such as: 'covid', 'covid-19'
but for the keyword 'alon' the engine can return articles with the word 'alone' in their title. For these scenarios there’s the full match option, so the engine will return articles with the exact sequence only.


ENJOY:)
'''


import ast
import requests
import smtplib, ssl
from datetime import date

#my API_key
api_key = '68c1a896eb0143e181b3a7543efcc60b'

# getting the most update data (articles on the main page only)
def news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=68c1a896eb0143e181b3a7543efcc60b'
    news = requests.get(url).json()
    return news
articles = news()
articles = articles['articles']

''' For QA only
with open('raw_data', 'w') as f:
    f.write(str(articles)[1:-1])
'''
# writing\overwriting a file with the most update data (articles on the main page only)
with open('raw_data_if_new', 'w') as f:
    f.write(str(articles)[1:-1])

with open('raw_data_if_new') as f:
    origin_info_if_new = f.read()

# getting all history of articles from an exiting file and save it as a list
with open('raw_data') as f:
    origin_info = f.read()
bank_of_articles = ast.literal_eval(origin_info)
bank_of_articles_if_new = ast.literal_eval(origin_info_if_new)


# adding new articles to bank_of_articles(raw data) - only if the bank is not the most updated.
def add_articles(bank_of_articles, new_articles):
    signal = False  # variable that indicates if the most updated data is in the bank or not.
    for article in bank_of_articles:
        if article in new_articles:
            signal = True
    if signal:
        return bank_of_articles  # which means that the articles on the main page are in the bank.
    else:
        # adding the new articles to the bank
        with open('raw_data', 'a') as f:
            f.write(', ' + str(articles)[1:-1])

        return bank_of_articles + bank_of_articles_if_new


bank_of_articles = add_articles(bank_of_articles, bank_of_articles_if_new)  # now the bank is most updated.

print(bank_of_articles_if_new)  # qa only
print(len(bank_of_articles))  # qa only

# Getting input from user
keywords = input("Insert your keywords ").replace(",", " ").split()
name = input("\nWhat is your name?").title()
match = input('Insert 1 for a partial match and 2 a for full match')
while match not in ['1', '2']:
    match = input('Amit don\'t play with me, insert 1 or 2 :)')
date_of_publication = input('Optional: Insert a date of publication in the following format "year-month-day", press 1 for today results only. (The default is anytime)')
if date_of_publication == '1':
    date_of_publication = str(date.today())


# initiate variables
# use during the main function to check and return all the keywords which is unfounded.
all_words_in_titles = str([bank_of_articles[article]['title'] for article in range(0, len(bank_of_articles))]).lower().title().replace(",","").replace("'", "").replace('"', "").replace('[', "").replace(']', "")
# presents the keywords as a list while each keyword begins with a big letter.
keywords = [word.lower().title() for word in keywords]

# presents only one keyword when the user enter the word twice, once begins with big letter and the other one with small letter.
keywords = set(keywords)


def articles_by_specific_date(bank_of_articles, date):

    articles_by_specific_date = []
    for article in bank_of_articles:

        if article['publishedAt'][:10] == date: #which means that the article published on the requested date.
            article_by_date = "[" + str(article) + "]"
            article_by_date = ast.literal_eval(article_by_date)
            articles_by_specific_date += article_by_date

    return articles_by_specific_date


def articles_partial_match(bank_of_articles, keywords):

    articles_by_partial_match = []
    for article in bank_of_articles:

        for keyword in keywords:
            if keyword in article['title'].lower().title(): #which means that partial match was founded.
                article_by_keyword = "[" + str(article) + "]"
                article_by_keyword = ast.literal_eval(article_by_keyword)
                articles_by_partial_match += article_by_keyword

    return articles_by_partial_match


def articles_full_match(bank_of_articles, keywords):

    articles_by_full_match = []
    for article in bank_of_articles:

        for keyword in keywords:
            if keyword in article['title'].lower().title().split():#which means that full match was founded.
                article_by_keyword = "[" + str(article) + "]"
                article_by_keyword = ast.literal_eval(article_by_keyword)
                articles_by_full_match += article_by_keyword

    return articles_by_full_match


def common_articles(list1, list2):
    common_articles = []
    for article in list1:

        if article in list2:
            article = "[" + str(article) + "]"
            article = ast.literal_eval(article)
            common_articles += article
    return common_articles


# main function
def api_news_articles(articles, keywords, match):

    msg = f'\nHi {name},\n\nFollowing are your resutls for these keywords: {str(keywords)[1:-1]}'
    list_of_missing_words = []
    if match == '1': # which means a partial match
        list_of_articles_by_match = articles_partial_match(bank_of_articles, keywords)
        all_words_in_titles = str([bank_of_articles[article]['title'] for article in range(0, len(bank_of_articles))]).lower().title().replace(",", "").replace("'","").replace('"', "").replace('[', "").replace(']', "")

    elif match == '2': #which means a full match
        list_of_articles_by_match = articles_full_match(bank_of_articles, keywords)
        all_words_in_titles = str([bank_of_articles[article]['title'] for article in range(0, len(bank_of_articles))]).lower().title().replace(",", "").replace("'","").replace('"', "").replace('[', "").replace(']', "").split()

    if date_of_publication != '': #which means that the user wants article for a specific date only.
        list_of_articles_by_date = articles_by_specific_date(bank_of_articles, date_of_publication)

    else: # use all the bank of articles
        list_of_articles_by_date = bank_of_articles
    # filtered bank of articles according to user's choice
    final_bank_of_articles = common_articles(list_of_articles_by_date, list_of_articles_by_match)

    for keyword in keywords:

        if keyword not in all_words_in_titles:
            list_of_missing_words.append(keyword)

        else:
            index = 1
            msg += f'\n\nFor the keyword {keyword}:\n'
            for article in final_bank_of_articles:

                if keyword in article['title'].lower().title():
                    msg +=f"\n{index}. Title: {article['title']}:\n{article['url']}\n\n{article['publishedAt'][:10]} {article['publishedAt'][11:-1]}\n{100 * '-'}"
                    index += 1

    if list_of_missing_words == list(keywords):
        msg += '\n\nSorry we couldn\'t find any articles for your keywords, you\'re welcome to try another keyword'
    elif list_of_missing_words != []:
        msg += f'\n\n*** Sorry but we couldn\'t find any results for:{list_of_missing_words}'

    return msg

msg = api_news_articles(articles, keywords,match)
print(msg)

'''
#sending the result by email
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "project.naya4040@gmail.com"  # Enter your address
receiver_email = 'alonb4040@gmail.com'  # Enter receiver address
password = 'Naya4040'
subject = 'NEWS FOR YOU'
body = msg
message = f'subject: {subject}\n\n{body}'

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

'''





