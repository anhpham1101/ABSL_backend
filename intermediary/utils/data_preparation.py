from preprocessing.lexicon.r_words import emo, phone_keywords, shirt_keywords
import preprocessing.preprocessing as prcs

class DataPreprocess:
    def __init__(self, product_type_id, comments):
        # Initial
        self.comments = comments
        self.product_type_id = product_type_id
        self.keyword = shirt_keywords if product_type_id == 1 else phone_keywords
        self.comment_ids = [x.get('commentId') for x in comments]
        self.comments_content = [x.get('comment') for x in comments]
        # Preprocess
        self.data_char = []
        self.data_word = []
    
    def preprocess_data_word(self):
        preprocessed_data = prcs.InferencePreparation(
            self.comments,
            'preprocessing/lexicon/ecom_vocab.pkl',
            100,
            emojis=emo,
            keywords=self.keyword
        ).run()
        X = preprocessed_data.get('X_test', False)
        X_mask = preprocessed_data.get('X_test_mask', False)
        self.data_word = [{"input": X[i].tolist(), "input_mask": X_mask[i].tolist()} for i, comment_id in enumerate(self.comment_ids)]

    def preprocess_data_char(self):
        preprocessed_data = prcs.InferencePreparation(
            self.comments,
            'preprocessing/lexicon/char_vocab.pkl',
            310,
            'content',
            'gibb',
            emojis=None,
            keywords=None,
            char_level=True
        ).run()
        X = preprocessed_data.get('X_test', False)
        X_mask = preprocessed_data.get('X_test_mask', False)
        self.data_char = [{"input": X[i].tolist(), "input_mask": X_mask[i].tolist()} for i, comment_id in enumerate(self.comment_ids)]
    
    def update_data(self):
        for i in range(len(self.comments)):
            self.comments[i].update({
                'data_word': self.data_word[i],
                'data_char': self.data_char[i]
            })

    ''' Preprocess data
    :param option -- ['all', 'gibb', 'other']:
    :return:
        'all': return both preprocess data on char and word level
        'gibb': return preprocess data on char level with id
        'other': return preprocess data on word level with id
    '''
    def run(self, option):
        if option == 'all':
            self.preprocess_data_char()
            self.preprocess_data_word()
            self.update_data()
            return self.comments
        elif option == 'gibb':
            self.preprocess_data_char()
            return self.comment_ids, self.data_char
        elif option == 'other':
            self.preprocess_data_word()
            return self.comment_ids, self.data_word
