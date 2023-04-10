import gensim
import re
import spacy

from spacy.lang.en import English



nlp = spacy.load("en_core_web_lg")
#nlp = en_core_web_sm.load(disable=['parser','ner'])
lda_model7=gensim.models.ldamodel.LdaModel.load("nlp_models/lda_model_7_30Percent")

def my_lemmatizer(doc):
    return [ w.lemma_.lower() for w in nlp(doc)
                      if w.pos_ not in ['PUNCT', 'SPACE', 'SYM', 'CCONJ', 'NUM']
                      and w.lemma_ not in ['_', '.'] ]

stopwords = spacy.lang.en.stop_words.STOP_WORDS
stopwords.union(['-pron-'])
stopwords = set(my_lemmatizer(' '.join(list(stopwords))))

stop_words = ["restaurant", "bar", "drink", "pancake", "apple", "order", "try", "brisket", "tuna", "lamb", "grill",
              "carne", "dip", "dip","chop", "broth", "breakfast", "salsa", "brunch", "cafe", "juice", "asada", "roast",
              "list", "wall","vegetarian", "phoenix", "buffet","lunch", "dinner", "probably", "maybe", "mango", "hummus",
              "wrap", "tempura", "duck", "wing", "meat", "bbq", "pie", "pickle", "chili", "turkey", "shake", "bagel",
              "ranch", "bake", "bone", "honey", "buffalo", "mozzarella", "belly", "girl", "guy", "husband", "wife",
              "pizza", "shrimp", "chicken", "fry", "que", "est", "san", "les", "pas", "une", "tre", "des", "sont", "vous",
              "cest", "vegetable", "resto", "prix", "las", "sur", "rice", "thai", "noodle", "beef", "chinese", "bowl", "pho",
              "raman", "roll", "curry", "korean", "tea", "vietnamese", "kimchi", "dim", "bean", "teriyaki", "egg", "tofu",
              "pork", "beef", "soup", "cheese", "pasta", "sandwich", "macaroni", "burrito", "salad", "cheese", "bread",
              "sandwich", "pepperoni", "crust", "capriottis", "burger", "beer", "milkshake", "tomato", "greek", "italian",
              "lettuce", "gyro", "veggie", "pita", "pizzeria", "ketchup", "hamburger", "cheeseburger", "garlic", "onion",
              "meatball", "mushroom", "spaghetti", "spinach", "caesar", "salmon","lasagna", "parmesan", "bruschetta", "choose",
              "avocado", "cucumber", "sushi", "crab", "vegas", "oyster", "sashimi", "lobster", "japanese", "person","sausage",
              "omelette", "benedict", "muffin", "skillet", "brownie", "cuban", "croissant", "taco","mexican", "chip", "salsa"
              "burrito", "tacos", "tortilla", "margarita", "rice", "nacho", "corn", "enchilada","chipotle", "quesadilla",
              "carnitas", "guacamole", "queso", "guac", "fajita", "mexico", "pico", "donut", "strawberry","fruit", "cream",
              "ice", "banana", "lady", "men","crepe", 'butter', "orange", "smoothie", "chocolate", "coconut", "cheesecake",
              "almond", "espresso", "maple", "syrup","peach", "nutella", "pudding", "lemon", "orange", "creme", "caramel",
              "cookie", "indian", "steak", "scallop", "cake","potato", "jalapeno", "nobu" "tuna", "poke", "ayce", "dumpling",
              "coleslaw", "fish", "sauce", "roti","curd", "chimichanga","macaron", "hamachi", "seaweed", "cilantro", "hawaiian",
              "mackerel", "soda", "rib", "coffee", "french","poutine", "gravy", "bakery", "vanilla", "cheddar", "german",
              "jam", "american", "bento", "http", "macaroon", "tout", "com","montreal", "waffle","s", "bacon", "toast", "soy",
              "poke", "toffee", "mandalay", "yelp", "latte", "sugar", "biscuit", "ham", "scramble", "seafood", "filet", "know",
              "calamari", "cilantro", "hamachi", "miso", "oven", "dough", "gluten", "vegan", "guacamole", "margaritas",
              "wine", "pastrami", "deli", "chowder", "steakhouse", "mex", "ribeye", "ribeye", "strip", "hotel", "dog",
              "mall", "station", "casino", "hot", "asian", "foie", "gelato", "bellagio", "center", "shopping", "elevator",
              "venetian", "tower", "lamp","grand", "palazzo", "chai", "mussel"]

#tokenize the review text
def process_words(texts, stop_words=set(), allowed_pos=['NOUN', 'PROPN','ADJ', 'VERB', 'ADV']):
    result = []
    for t in texts:
        t = re.sub('\'', '', t)  #  replace single quotation marks (mainly to capture contractions)
        t = gensim.utils.simple_preprocess(t, deacc=True, min_len=3)
        doc = nlp(' '.join(t))
        result.append([token.lemma_ for token in doc if token.pos_ in allowed_pos and
                       token.lemma_ not in stop_words])
    return result

stopwords_include_food=stopwords.union(stop_words)

class_label={0:'Service',
             1:'Atmosphere',
             2:'Food/Value',
             3:'Food',
             4:'Postive experience',
             5:'Overall experience',
             6:'Value/Experience'}


#Food, Service, Atmosphere, Value for Food, Value for Overall Experience
def ReviewTopicClassifer(Reviews_array, lda_model=lda_model7, class_labels=class_label):
    # tokenize the review
    processed_new = process_words(Reviews_array, stop_words=stopwords_include_food.union(['-adj-']))
    corpus = []
    # convert the tokenized reviews to list of corpus
    for i in processed_new:
        new_text_corpus = lda_model.id2word.doc2bow(i)
        corpus.append(new_text_corpus)

    pred_topic_classes = []
    for review_j in corpus:
        pred_class = lda_model.get_document_topics(review_j)
        pred_topic_classes.append(pred_class)

    # change the class number to label
    return_classes = []
    for classifed_review in pred_topic_classes:
        temp = []
        for i in classifed_review:
            label = class_labels[i[0]]
            temp.append((label, i[1]))
        return_classes.append(dict(temp))

    return return_classes


