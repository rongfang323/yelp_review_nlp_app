# yelp_review_nlp_app
yelp_review_nlp_app is a web-based app that refined the current yelp recommendation list by allowing the user to select the most relevant features they are looking into the restaurants. The app used topic-based sentimental analysis read through over 30,000 reviews provided by yelp open data sourse and extracted their evaluation regarding the restaurants' food, service, atmosphere, value for food, value for overall experience. The recommendation list pushed by the app is sorted in ascending order by the percentage of postive votes for the chosen features. 

# Link
Please find the link to the app https://yummishi.herokuapp.com/

# Dependencies
The code is written in Python 3.8. You will need:
pandas==1.1.1
numpy==1.19.1
spacy==2.3.2
requests==2.24.0
pyLDAvis==2.1.2
gunicorn==20.0.4
gensim==3.8.3
Flask==1.1.2
dill==0.3.2
scikit-learn==0.23.2
en_core_web_sm-2.2.0
regex==2020.7.14
