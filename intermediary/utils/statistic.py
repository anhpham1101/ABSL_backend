from request_model import Gibb, Shirt, Phone, Other
from static.aspect_definition import aspect_definition
from math import ceil
from time import time

NUM_COMMENT_PER_BATCH = 500

def error(func):
    def handlingError(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
    return handlingError


''' Summary how many sentences contain gibberish words and are advertising for coins
    :param:
        ::product_type_id:: need for calling API to model
        ::comments:: preprocessed comments
    :return:
        ::other:: number of comments are advertising for coins
        ::gib:: number of comments contain gibberish words
        ::total:: total comments has been processed
        ::rating_total:: total comments after removing sentences with gibberish words
        ::rating_count:: details rating of comments
        ::return_data:: return comments after removing sentences with gibberish words
'''
class SummaryStatistic:
    def __init__(self, product_type_id, comments):
        # Preload
        self.product_type_id = product_type_id
        self.comments = comments

        # Statistic
        self.other = 0
        self.gib = 0
        self.total = len(comments)
        self.rating_count = [0, 0, 0, 0, 0]
        self.rating_total = 0

    def _get_gib(self):
        data_preprocessed_char = [x.get('data_char') for x in self.comments]
        batch_num = ceil(float(len(data_preprocessed_char)) / NUM_COMMENT_PER_BATCH)
        predict_data = []
        for i in range(0, batch_num):
            start = i * NUM_COMMENT_PER_BATCH
            end = (i + 1) * NUM_COMMENT_PER_BATCH or len(data_preprocessed_char)
            request_data = data_preprocessed_char[start : end]
            predict_data += Gibb(request_data).predict()
        self.gib = len(list(filter(lambda r: r.get('other') == 1, predict_data)))
        
        for i in range(len(self.comments)):
            self.comments[i].update(predict_data[i])
        
        # Sentence with gibb word will be removed out of statistic
        self.comments = list(filter(lambda r: r.get('other') == 0, self.comments))
    
    def _get_other(self):
        data_preprocessed_word = [x.get('data_word') for x in self.comments]
        batch_num = ceil(float(len(data_preprocessed_word)) / NUM_COMMENT_PER_BATCH)
        predict_data = []
        for i in range(0, batch_num):
            start = i * NUM_COMMENT_PER_BATCH
            end = (i + 1) * NUM_COMMENT_PER_BATCH or len(data_preprocessed_word)
            request_data = data_preprocessed_word[start : end]
            predict_data += Other(request_data).predict()
        self.other = len(list(filter(lambda r: r.get('other') == 1, predict_data)))
    
    def _comment_type_chart_statistic(self):
        self._get_gib()
        self._get_other()

    def _summary_chart_statistic(self):
        for i in range(1, 6):
            self.rating_count[i - 1] = len(list(filter(lambda r: r.get('rating') == i, self.comments)))
        self.rating_count.reverse()
        self.rating_total = sum(self.rating_count)

    def run(self):
        print('========== Statistic summary analysis ==========')
        self._comment_type_chart_statistic()
        self._summary_chart_statistic()
        return {
            'other': self.other,
            'gib': self.gib,
            'total': self.total,
            'rating_total': self.rating_total,
            'rating_count': self.rating_count,
            'return_data': self.comments
        }

''' Summary sentiment for each aspect of product
    :param:
        ::product_type_id:: need for calling API to model
        ::comments:: preprocessed comments
    :return:
        ::aspects:: list of aspect labels
        ::pos:: list of positive group by aspect
        ::neu:: list of neutral group by aspect
        ::neg:: list of negative group by aspect
'''
class SentimentStatistic:
    def __init__(self, product_type_id, comments):
        # Preload
        self.product_type_id = product_type_id
        self.comments = comments

        # Statistic
        self.aspects = []
        self.pos = []
        self.neu = []
        self.neg = []

    def _stackbar_chart_statistic(self):
        data_preprocessed_word = [x.get('data_word') for x in self.comments]
        batch_num = ceil(float(len(data_preprocessed_word)) / NUM_COMMENT_PER_BATCH)
        comments_sentiment_predict = []
        for i in range(0, batch_num):
            start = i * NUM_COMMENT_PER_BATCH
            end = (i + 1) * NUM_COMMENT_PER_BATCH or len(data_preprocessed_word)
            request_data = data_preprocessed_word[start : end]
            if self.product_type_id == 1:
                Model = Shirt(request_data)
            elif self.product_type_id == 2:
                Model = Phone(request_data)
            comments_sentiment_predict += Model.predict()
        self.aspects = list(map(lambda r: r.get("as"), aspect_definition.get(self.product_type_id).get("aspect")))
        # Statistic by aspect
        aspects = enumerate(self.aspects)
        self.pos = [0] * len(self.aspects)  
        self.neu = [0] * len(self.aspects)
        self.neg = [0] * len(self.aspects)
        for index, aspect in aspects:
            self.pos[index] = len(list(filter(lambda r: r == 1, [x.get(aspect) for x in comments_sentiment_predict])))
            self.neu[index] = len(list(filter(lambda r: r == 2, [x.get(aspect) for x in comments_sentiment_predict])))
            self.neg[index] = len(list(filter(lambda r: r == 3, [x.get(aspect) for x in comments_sentiment_predict])))

    def run(self):
        print('========== Statistic sentiment analysis ==========')
        self._stackbar_chart_statistic()
        return {
            'positive': self.pos,
            'neutral': self.neu,
            'negative': self.neg
        }
