#import request as request
from flask import Flask, render_template, request, flash
from yelpRequest import query_api, requestReviews, get_business, BUSINESS_PATH, API_KEY, API_HOST
from topic_sentiment_classifier import TopicSentimental, OrderBusiness, BayesianSmooth, OrderBusiness_new
import pandas as pd



app = Flask(__name__)
app.debug = True

@app.route('/')
def index():

    return render_template('index.html')

"""Once users input the terms for restaurant searching, 
   the web return a list of searched result"""




@app.route('/listings', methods=['POST'])
def search_results():



    cateInput = request.form['category_search']
    locInput = request.form['location_search']
    topSelect = request.form['orderByValSelected']

    #return the search results
    if not cateInput or not locInput or not topSelect:
       cateInput='Brunch'
       locInput='Eugene, OR'

    results = query_api(cateInput, str(locInput), 15)


    #acquire the business id and the path to request the review
    restaurant_id = [i['id'] for i in results]
    business_path = [BUSINESS_PATH + id for id in restaurant_id]

    #aquire the three reviews of each business
    reviews_by_business = []
    for i in business_path:
        new_reviews = requestReviews(i)
        new_reviews_text = [review['text'] for review in new_reviews['reviews']]
        reviews_by_business.append(new_reviews_text)

    #classify the review into predefined topic and the attitudes of the reviews
    review_topic_by_business = []

    for reviews in reviews_by_business:
        review_topic_by_business.append(TopicSentimental(topSelect, reviews))

    #add the selected topic and the number of votes to the business dict for each business
    for i in range(len(results)):
        results[i][list(review_topic_by_business[i].keys())[0]] = list(review_topic_by_business[i].values())[0]

    # arrange the search results based on the number of positive reviews of the selected topic
    businessOrdered=OrderBusiness_new(topSelect, results)

    categories = []
    address = []
    name = []
    url_yelp = []
    url_image = []
    ratings = []
    id = []
    postive_vote=[]
    negative_vote=[]

    liked=' reviews liked the ' + str(topSelect)
    disliked=' reviews disliked the ' + str(topSelect)

    for i in businessOrdered:
        categories.append(i['categories'])
        address.append(i['location']['display_address'][0])
        print(i['location'])
        name.append(i['name'])
        url_yelp.append(i['url'])
        #url_image.append(i['photos'])
        ratings.append(i['rating'])
        id.append(i['id'])
        url_image.append(i['image_url'])
        if topSelect !='Star Rating':
           postive_vote.append(str(i[topSelect]['Positive']) + liked)
           negative_vote.append(str(i[topSelect]['Negative']) + disliked)
        else:
            postive_vote.append(str(i[topSelect]['Positive']) + ' like here.')
            negative_vote.append(str(i[topSelect]['Negative']) + ' disliked here.')

    search_result_text=str(cateInput)+" restaurant recommendation by " + str(topSelect) + ' in ' + str(locInput)

    #url = "https://s3-media2.fl.yelpcdn.com/bphoto/avpDoE_YOrxKqut0zr914w/o.jpg"
    return render_template('listings.html', search_result_text=search_result_text,
                           review1_up=postive_vote[0], review1_down=negative_vote[0],
                           review2_up=postive_vote[1], review2_down=negative_vote[1],
                           review3_up=postive_vote[2], review3_down=negative_vote[2],
                           review4_up=postive_vote[3], review4_down=negative_vote[3],
                           review5_up=postive_vote[4], review5_down=negative_vote[4],
                           review6_up=postive_vote[5], review6_down=negative_vote[5],
                           review7_up=postive_vote[6], review7_down=negative_vote[6],
                           review8_up=postive_vote[7], review8_down=negative_vote[7],
                           review9_up=postive_vote[8], review9_down=negative_vote[8],
                           review10_up=postive_vote[9], review10_down=negative_vote[9],
                           review11_up=postive_vote[10], review11_down=negative_vote[10],
                           review12_up=postive_vote[11], review12_down=negative_vote[11],
                           review13_up=postive_vote[12], review13_down=negative_vote[12],
                           review14_up=postive_vote[13], review14_down=negative_vote[13],
                           review15_up=postive_vote[14], review15_down=negative_vote[14],
                           name1=name[0], name2=name[1], name3=name[2],
                           name4=name[3], name5=name[4], name6=name[5],
                           name7=name[6], name8=name[7], name9=name[8],
                           name10=name[9], name11=name[10], name12=name[11],
                           name13=name[12], name14=name[13], name15=name[14],
                           ulr_yelp1=url_yelp[0], ulr_yelp2=url_yelp[1], ulr_yelp3=url_yelp[2],
                           ulr_yelp4=url_yelp[3], ulr_yelp5=url_yelp[4], ulr_yelp6=url_yelp[5],
                           ulr_yelp7=url_yelp[6], ulr_yelp8=url_yelp[7], ulr_yelp9=url_yelp[8],
                           ulr_yelp10=url_yelp[9], ulr_yelp11=url_yelp[10], ulr_yelp12=url_yelp[11],
                           ulr_yelp13=url_yelp[12], ulr_yelp14=url_yelp[13], ulr_yelp15=url_yelp[14],
                           url1=url_image[0],url2=url_image[1],url3=url_image[2],
                           url4=url_image[3],url5=url_image[4],url6=url_image[5],
                           url7=url_image[6],url8=url_image[7],url9=url_image[8],
                           url10=url_image[9], url11=url_image[10], url12=url_image[11],
                           url13=url_image[12], url14=url_image[13], url15=url_image[14],
                           rate1=ratings[0], rate2=ratings[1], rate3=ratings[2],
                           rate4=ratings[3], rate5=ratings[4], rate6=ratings[5],
                           rate7=ratings[6], rate8=ratings[7], rate9=ratings[8],
                           rate10=ratings[9], rate11=ratings[10], rate12=ratings[11],
                           rate13=ratings[12], rate14=ratings[13], rate15=ratings[14],
                           address1=address[0], address2=address[1], address3=address[2],
                           address4=address[3], address5=address[4], address6=address[5],
                           address7=address[6], address8=address[7], address9=address[8],
                           address10=address[9], address11=address[10], address12=address[11],
                           address13=address[12], address14=address[13], address15=address[14]
                           )

@app.route('/how-it-works')
def how_it_works():
    return render_template('how-it-works.html')

@app.route('/Demo', methods = ['GET','POST'])
def demo():
    business_demo = pd.read_csv('business_review_demo.csv')

    if request.method == 'POST':

       cateInput = request.form['category_search']
       locInput = request.form['location_search']
       topSelect = request.form['orderByValSelected']

       print('there')
    # return the search results
    else:
        cateInput = 'Chinese'
        locInput = 'Phoenix, AZ'
        topSelect = 'Food'
        print('here')

    print(cateInput)
    print(locInput)
    print(topSelect)
    #request business information from yelp website
    business_selected=business_demo[business_demo.categories==cateInput][business_demo.city==str(locInput).split(',')[0]]

    print(business_selected)
    business_id_demo=list(business_selected.business_id.unique())
    results = []
    for i in business_id_demo:
        results.append(get_business(API_KEY, i))

    # acquire all reviews of each business from the business_demo dataset
    reviews_by_business = []
    for i in business_id_demo:
        new_reviews = business_demo[business_demo['business_id']==i]
        new_reviews_text = list(new_reviews['text'])
        reviews_by_business.append(new_reviews_text)

    # classify the review into predefined topic and the attitudes of the reviews
    review_topic_by_business = []
    review_num = []
    for reviews in reviews_by_business:
        review_num.append(len(reviews))
        review_topic_by_business.append(TopicSentimental(topSelect, reviews))

    # add the selected topic and the number of votes to the business dict for each business
    for i in range(len(results)):
        results[i]['number of reviews'] = review_num[i]
        results[i][list(review_topic_by_business[i].keys())[0]] = list(review_topic_by_business[i].values())[0]

    print(results)
    # arrange the search results based on the number of positive reviews of the selected topic
    businessOrdered = OrderBusiness(topSelect, results)

    categories = []
    address = []
    name = []
    url_yelp = []
    url_image = []
    ratings = []
    id = []
    positive_vote = []
    negative_vote = []

    liked = ' % reviews liked the ' + str(topSelect)
    disliked = ' % reviews disliked the ' + str(topSelect)

    for i in businessOrdered:
        categories.append(i['categories'])
        address.append(i['location']['display_address'][0])
        print(i['location'])
        name.append(i['name'])
        url_yelp.append(i['url'])
        # url_image.append(i['photos'])
        ratings.append(i['rating'])
        id.append(i['id'])
        url_image.append(i['image_url'])
        if topSelect != 'Star Rating':
            str_positive='Adjusted ' + str(BayesianSmooth(i['number of reviews'],
                                                            i[topSelect]['Positive'],
                                                            len(businessOrdered))) + liked
            str_negative = 'Adjusted ' + str(BayesianSmooth(i['number of reviews'],
                                                           i[topSelect]['Negative'],
                                                           len(businessOrdered))) + disliked
            positive_vote.append(str_positive)
            negative_vote.append(str_negative)
        else:
            str_positive = 'Adjusted ' + str(BayesianSmooth(i['number of reviews'],
                                                           i[topSelect]['Positive'],
                                                           len(businessOrdered))) + ' % reviews like here.'
            str_negative = 'Adjusted ' + str(BayesianSmooth(i['number of reviews'],
                                                           i[topSelect]['Negative'],
                                                           len(businessOrdered))) + ' % reviews disliked here.'
            positive_vote.append(str_positive)
            negative_vote.append(str_negative)

    print(positive_vote)
    print(len(businessOrdered))

    if len(businessOrdered) < 18:
        for _ in range(len(businessOrdered), 18):
           categories.append('No more search result')
           address.append('No more search result')
           name.append('No more search result')
           url_yelp.append('https://www.yelp.com/search?find_desc=&find_loc='+str(locInput)+'%2C+OR&ns=1')
           # url_image.append(i['photos'])
           ratings.append('0')
           url_image.append("{{url_for('static', filename='img/arrange/arrange-1.png')}}")
           positive_vote.append('No result to show.')
           negative_vote.append('No result to show.')

    print(len(categories))

    search_result_text = str(cateInput) + " restaurant recommendation by " + str(topSelect) + ' in ' + str(locInput)

    return render_template('Demo.html', search_result_text=search_result_text,
                           review1_up=positive_vote[0], review1_down=negative_vote[0],
                           review2_up=positive_vote[1], review2_down=negative_vote[1],
                           review3_up=positive_vote[2], review3_down=negative_vote[2],
                           review4_up=positive_vote[3], review4_down=negative_vote[3],
                           review5_up=positive_vote[4], review5_down=negative_vote[4],
                           review6_up=positive_vote[5], review6_down=negative_vote[5],
                           review7_up=positive_vote[6], review7_down=negative_vote[6],
                           review8_up=positive_vote[7], review8_down=negative_vote[7],
                           review9_up=positive_vote[8], review9_down=negative_vote[8],
                           review10_up=positive_vote[9], review10_down=negative_vote[9],
                           review11_up=positive_vote[10], review11_down=negative_vote[10],
                           review12_up=positive_vote[11], review12_down=negative_vote[11],
                           review13_up=positive_vote[12], review13_down=negative_vote[12],
                           review14_up=positive_vote[13], review14_down=negative_vote[13],
                           review15_up=positive_vote[14], review15_down=negative_vote[14],
                           review16_up=positive_vote[15], review16_down=negative_vote[15],
                           review17_up=positive_vote[16], review17_down=negative_vote[16],
                           review18_up=positive_vote[17], review18_down=negative_vote[17],
                           name1=name[0], name2=name[1], name3=name[2],
                           name4=name[3], name5=name[4], name6=name[5],
                           name7=name[6], name8=name[7], name9=name[8],
                           name10=name[9], name11=name[10], name12=name[11],
                           name13=name[12], name14=name[13], name15=name[14],
                           name16=name[15], name17=name[16], name18=name[17],
                           ulr_yelp1=url_yelp[0], ulr_yelp2=url_yelp[1], ulr_yelp3=url_yelp[2],
                           ulr_yelp4=url_yelp[3], ulr_yelp5=url_yelp[4], ulr_yelp6=url_yelp[5],
                           ulr_yelp7=url_yelp[6], ulr_yelp8=url_yelp[7], ulr_yelp9=url_yelp[8],
                           ulr_yelp10=url_yelp[9], ulr_yelp11=url_yelp[10], ulr_yelp12=url_yelp[11],
                           ulr_yelp13=url_yelp[12], ulr_yelp14=url_yelp[13], ulr_yelp15=url_yelp[14],
                           ulr_yelp16=url_yelp[15], ulr_yelp17=url_yelp[16], ulr_yelp18=url_yelp[17],
                           url1=url_image[0], url2=url_image[1], url3=url_image[2],
                           url4=url_image[3], url5=url_image[4], url6=url_image[5],
                           url7=url_image[6], url8=url_image[7], url9=url_image[8],
                           url10=url_image[9], url11=url_image[10], url12=url_image[11],
                           url13=url_image[12], url14=url_image[13], url15=url_image[14],
                           url16=url_image[15], url17=url_image[16], url18=url_image[17],
                           rate1=ratings[0], rate2=ratings[1], rate3=ratings[2],
                           rate4=ratings[3], rate5=ratings[4], rate6=ratings[5],
                           rate7=ratings[6], rate8=ratings[7], rate9=ratings[8],
                           rate10=ratings[9], rate11=ratings[10], rate12=ratings[11],
                           rate13=ratings[12], rate14=ratings[13], rate15=ratings[14],
                           rate16=ratings[15], rate17=ratings[16], rate18=ratings[17],
                           address1=address[0], address2=address[1], address3=address[2],
                           address4=address[3], address5=address[4], address6=address[5],
                           address7=address[6], address8=address[7], address9=address[8],
                           address10=address[9], address11=address[10], address12=address[11],
                           address13=address[12], address14=address[13], address15=address[14],
                           address16=address[15], address17=address[16], address18=address[17]
                           )



@app.route('/About')
def about():
    return render_template('About.html')

@app.route('/personal_profile')
def personal_profile():
    return render_template('personal_profile.html')



if __name__ == '__main__':
    app.run(port=33568, debug=True)



