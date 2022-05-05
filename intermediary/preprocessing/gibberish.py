import pickle
import math


class Gibberish:
    def __init__(self):
        self.model_data = pickle.load(open('preprocessing/gibberish/gib_model.pki', 'rb'))
        self.model_mat = self.model_data.get('mat')
        self.threshold = 0.04949999999999982
        self.accepted_chars = 'aáàảãạăắằẳẵặâấầẩẫậbcdđeéèẻẽẹêếềểễệfghiíìỉĩịjklmnoóòỏõọôốồổỗộơớờởỡợpqrstuúùủũụưứừửữựvxyz '
        self.pos = dict([(char, idx) for idx, char in enumerate(self.accepted_chars)])

    def normalize(self, line):
        return [c.lower() for c in line if c.lower() in self.accepted_chars]

    def ngram(self, n, l):
        filtered = self.normalize(l)
        for start in range(0, len(filtered) - n + 1):
            yield ''.join(filtered[start:start + n])

    def avg_transition_prob(self, l):
        """ Return the average transition prob from l through log_prob_mat. """
        log_prob = 0.0
        transition_ct = 0
        for a, b in self.ngram(2, l):
            log_prob += self.model_mat[self.pos[a]][self.pos[b]]
            transition_ct += 1

        # Consider short sentence is not gibberish
        if len(l) <= 10:
            log_prob = 1
            
        # The exponentiation translates from log probs to probs.
        return math.exp(log_prob / (transition_ct or 1))

    def check_gibberish(self, text):
        return self.avg_transition_prob(text) < self.threshold
    
    def count_giberish(self, texts):
        gibb_predict = [int(self.avg_transition_prob(text) < self.threshold) for text in texts]
        return gibb_predict
