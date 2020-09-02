from topic_classifer import ReviewTopicClassifer
import dill


sentimental_model=dill.load(open('nlp_models/sentimental_model.pkd', 'rb'))
class_label={0:'Service',
             1:'Atmosphere',
             2:'Food/Value',
             3:'Food',
             4:'Postive experience',
             5:'Overall experience',
             6:'Value/Experience'}


def TopicSentimental(topic, Review_array,   sentimental_model=sentimental_model):
    topic_class = ReviewTopicClassifer(Review_array)
    sentimental = sentimental_model.predict(Review_array)

    if topic == 'Star Rating':
        positive_count = 0
        negative_count = 0

        for review in sentimental:
            if review == 'Positive':
                positive_count += 1
            elif review == 'Negative':
                negative_count += 1

        return {topic: {'Positive': positive_count, 'Negative': negative_count}}

    if topic == 'Food':

        positive_count = 0
        negative_count = 0
        i = 0

        for review in topic_class:
            if 'Food' in review.keys() and review['Food'] > 0.10:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
            i += 1

        return {topic: {'Positive': positive_count, 'Negative': negative_count}}

    elif topic == 'Service':

        positive_count = 0
        negative_count = 0
        i = 0

        for review in topic_class:
            if 'Postive experience' in review.keys() and review['Postive experience'] > 0.1:
                postive_count = +1
                i += 1
                continue

            if 'Service' in review.keys() and review['Service'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            if 'Service' in review.keys() and 'Overall expereince' in review.keys() and \
                    review['Overall expereince'] + review['Service'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            if 'Service' in review.keys() and 'Value/Experience' in review.keys() and \
                    review['Value/Experience'] + review['Service'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            i += 1

        return {topic: {'Positive': positive_count, 'Negative': negative_count}}

    elif topic == 'Atmosphere':

        positive_count = 0
        negative_count = 0
        i = 0

        for review in topic_class:
            if 'Atmosphere' in review.keys() and 'Postive experience' in review.keys() and \
                    review['Postive experience'] + review['Atmosphere'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            if 'Atmosphere' in review.keys() and 'Overall expereince' in review.keys() and \
                    review['Overall expereince'] + review['Atmosphere'] > 0.3:
                positive_count = +1
                i += 1
                continue

            if 'Atmosphere' in review.keys() and 'Value/Experience' in review.keys() and \
                    review['Value/Experience'] + review['Atmosphere'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            i += 1

        return {topic: {'Positive': positive_count, 'Negative': negative_count}}

    elif topic == 'Value for Overall Experience':

        positive_count = 0
        negative_count = 0
        i = 0

        for review in topic_class:

            if 'Postive experience' in review.keys() and review['Postive experience'] > 0.3:
                positive_count = +1
                i += 1
                continue

            if 'Value/Experience' in review.keys() and 'Postive experience' in review.keys() and \
                    review['Postive experience'] + review['Value/Experience'] > 0.3:
                positive_count += 1
                i += 1
                continue

            if 'Overall expereince' in review.keys() and 'Postive experience' in review.keys() and \
                    review['Postive experience'] + review['Overall expereince'] > 0.3:
                positive_count += 1
                i += 1
                continue

            if 'Overall expereince' in review.keys() and review['Overall expereince'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            if 'Value/Experience' in review.keys() and review['Value/Experience'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            if 'Value/Experience' in review.keys() and 'Overall expereince' in review.keys() and \
                    review['Overall expereince'] + review['Value/Experience'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            i += 1

        return {topic: {'Positive': positive_count, 'Negative': negative_count}}


    elif topic == 'Value for Food':

        positive_count = 0
        negative_count = 0
        i = 0

        for review in topic_class:
            if 'Food/Value' in review.keys() and review['Food/Value'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            if 'Food' in review.keys() and 'Food/Value' in review.keys() and \
                    review['Food'] + review['Food/Value'] > 0.3:
                if sentimental[i] == 'Positive':
                    positive_count += 1
                if sentimental[i] == 'Negative':
                    negative_count += 1
                i += 1
                continue

            i += 1
        return {topic: {'Positive': positive_count, 'Negative': negative_count}}

# N is the total number of reviews for each business
# n is the number of positive votes for each business
# d is the total number of business
# alpha is the smoothing factor
def BayesianSmooth(N, n, d, alpha=1):
    return round((n+alpha)/(N+alpha*d)*100)

def OrderBusiness(topic, business):
    num_business=len(business)
    business_ordered = sorted(business, key=lambda x: x['rating'], reverse=True)
    business_ordered = sorted(business_ordered,
                              key= lambda x: BayesianSmooth(x['number of reviews'],
                                                            x[topic]['Positive'],
                                                            num_business), reverse=True)
    return business_ordered

def OrderBusiness_new(topic, business):
    business_ordered = sorted(business, key=lambda x: x['rating'], reverse=True)
    business_ordered = sorted(business_ordered, key= lambda x: x[topic]['Positive'], reverse=True)
    return business_ordered