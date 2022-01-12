# News search engine


Sending customized articles’ details to your Email address.
You can get articles based on keywords for your interest. The engine will search the entire articles’ bank, by titles, based on what’s relevant to your keywords. You can filter the web searches results, by a full match or a partial match and even by a specific date.


*Note - the script is insensitive (doesn't matter if you use upper-case\lower-case letters).


Partial match - searching for articles and sending all the articles that their title contains the sequence of the keyword. 
For example: for the keyword 'cov' the engine returns articles which in their title there׳s the sequence 'cov' such as: 'covid', 'covid-19' 
but for the keyword 'alon' the engine can return articles with the word 'alone' in their title. For these scenarios there’s the full match option, so the engine will return articles with the exact sequence only.

There are two text files:

1."raw_data" - which contains all the history of the articles.

2."raw_data_if_new - which after the run contains the most updated articles (Those on the main page only). During the script, we check if those articles are in "raw_data", if not, it adds them to it.


ENJOY:)


