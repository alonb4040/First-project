
'''
News engine search.

Sending customized articles details to an e-mail address. You can get articles based on the keywords that interest you. The engine will search the entire bank of articles, for only those whose titles are relevant to your keywords. You can filter by a full match or a partial match and even by a specific date.

*Note - the script is insensitive (doesn't matter if you use big\small letters).

Partial match - searching for articles and sending all the articles that their title contains the sequence of the keyword. For example: for the keyword 'cov' the engine returns articles which in their title there is the sequence 'cov' such as: 'covid', 'covid-19' but for the keyword 'alon' the engine can return articles with the word 'alone' in their title. For these scenarios there is the full match option, so the engine will return articles with the exact sequence only.

ENJOY:)
'''


import tkinter as tk
import ast
import requests
import smtplib
import ssl
from datetime import date

#GUI: creating all the widget
window = tk.Tk()
window.geometry("350x450")

#Title widget
Title_lable = tk.Label(text="NEWS search engine",bg = 'red', fg = 'white',width= 50)
Title_lable.pack()

#Keywords widgets
keywords_label = tk.Label(text="Insert your keywords",font=("ariel", 10))
keywords_label.pack()
entry_keywords = tk.Entry(fg="black", width=30,borderwidth=4)
entry_keywords.pack()

#name widgets
name_label = tk.Label(text="Insert your name",font=("ariel", 10))
name_label.pack()
entry_name = tk.Entry(fg="black", width=30,borderwidth=4)
entry_name.pack()
#email widgets
email_label = tk.Label(text="Insert your e-mail",font=("ariel", 10))
email_label.pack()
entry_email = tk.Entry(fg="black", width=30,borderwidth=4)
entry_email.pack()

#match widgets
match_label = tk.Label(text='Insert 1 for a partial match \n or 2 for a full match',font=("ariel", 10))
match_label.pack()
entry_match = tk.Entry(fg="black", width=30,borderwidth=4)
entry_match.pack()

# date_of_publication widgets
date_of_publication = tk.Label(text='Optional: Insert date of publication\n Insert 1 for today (The default is anytime)')
date_of_publication.pack()
entry_date_of_publication = tk.Entry(fg="black", width=30,borderwidth=4)
entry_date_of_publication.pack()

#my API_key
api_key = '68c1a896eb0143e181b3a7543efcc60b'

# getting the most update data (articles on the front page only)
def news():
    url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=68c1a896eb0143e181b3a7543efcc60b'
    news = requests.get(url).json()
    return news

articles = news()
articles = articles['articles']


# writing\overlapping a file with the most update data (articles on the front page only)
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


#this is the main function.
def api_main_function():
    # Getting input from user
    keywords = entry_keywords.get().replace(",", " ").split()
    keywords = [word.lower().title() for word in keywords]
    keywords = set(keywords)
    name =entry_name.get().title()
    match = entry_match.get()
    date_of_publication = entry_date_of_publication.get()

    if date_of_publication == '1':
        date_of_publication = str(date.today())


    #initiate the body of the mail. msg eaqual to the body of the mail. During the script msg gets all the output that we want to sent to the user.
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
                    msg +=f"\n{index}. Title: {article['title']}:\n{article['url']}\n{article['publishedAt'][:10]} {article['publishedAt'][11:-1]}\n{100 * '-'}"
                    index += 1
    if list_of_missing_words == list(keywords):
        msg += '\n\nSorry we couldn\'t find any articles for your keywords, you\'re welcome to try another keyword'
    elif list_of_missing_words != []:
        msg += f'\n\n*** Sorry but we couldn\'t find any results for:{list_of_missing_words}'

    print(msg)

    # sending the result by email
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "my.general.mail4040@gmail.com"  # Enter your address
    receiver_email = entry_email.get()  # Enter receiver address
    password = 'Naya4040'
    subject = 'NEWS FOR YOU'
    body = msg
    message = f'subject: {subject}\n\n{body}'

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return msg

# creating a button and assign the main function to it.
button = tk.Button(
    text="submit",
    width=25,
    height=5,
    fg="red",
    command = api_main_function)
button.pack()
window.mainloop()






