from utils.data_preparation import DataPreprocess
from request_model import Gibb, Other, Shirt, Phone
from utils.sentiment_mapping_value import TransformValue


class SentimentPredict:
    def __init__(self, product_type_id, comments):
        self.product_type_id = product_type_id
        self.comments = comments
        self.gib_sentences = []
        self.nor_sentences = []

    def _sentiment_predict(self):
        # Prepare data for gibb: char_level=True
        comment_ids, data_rq = DataPreprocess(self.product_type_id, self.comments).run(option='gibb')
        gibb_predict = Gibb(data_rq).predict()
        for i in range(len(self.comments)):
            if gibb_predict[i].get('other') == 1:
                self.comments[i].update({
                    'tagInfos': [{
                        "content": "Chứa ký tự vô nghĩa",
                        "textColor": "rgb(125, 125, 125)"
                    }]
                })
        # Remove sentences with gibb words and predict sentiments on them
        self.gib_sentences = list(filter(lambda r: r.get('tagInfos', None) != None, self.comments))
        self.comments = list(filter(lambda r: r.get('tagInfos', None) == None, self.comments))
        # Prepare data for other & sentiment: char_level=False
        comment_ids, data_rq = DataPreprocess(self.product_type_id, self.comments).run(option='other')
        other_predict = Other(data_rq).predict()
        if self.product_type_id == 1:
            SentimentModel = Shirt(data_rq)
        elif self.product_type_id == 2:
            SentimentModel = Phone(data_rq)
        sentiment_predict = SentimentModel.predict()

        for predict in zip(sentiment_predict, other_predict):
            predict[0].update(predict[1])

        transformer = TransformValue(comment_ids, sentiment_predict, self.product_type_id)
        self.nor_sentences = transformer.transform()

    def run(self):
        print('========== Sentiment prediction ==========')
        self._sentiment_predict()
        result = self.gib_sentences + self.nor_sentences
        return result
        