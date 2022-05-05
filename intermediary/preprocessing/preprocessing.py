import numpy as np
import preprocessing.preprocess.utils as putils
import preprocessing.preprocess.normalization_v2 as pnorm
import preprocessing.preprocess.tokenization as ptok
import preprocessing.preprocess.segmentation as pseg

import pickle
from sklearn.utils import Bunch

class Print:
    def warning(text):
        print(f'WARNING: {text}')
    def info(text):
        print(f'INFO: {text}')

class InferencePreparation:
  def __init__(self, test_set, vocabulary, input_length, content_name=None, label_names=None, emojis=None, keywords=None, char_level=False):
    self.test_set = test_set
    self.emojis = emojis
    self.keywords = keywords
    self.input_length = input_length
    with open(vocabulary, 'rb') as f:
      self.tokenizer = pickle.load(f).tokenizer

    self.char_level = char_level

    self.state= Bunch(
      X_test_mask = None,
      X_test = None,
      X_seg = None,
      y_test = None,
      content_name = content_name,
      label_names = label_names
    )

  def load(self):
    if isinstance(self.test_set, str):
      assert self.state.content_name is not None
      assert self.state.label_names is not None
      self.state.X_test, self.state.y_test = putils.csv_to_dataset(f'{self.test_set}', self.state.content_name, self.state.label_names)
    elif isinstance(self.test_set, list):
      self.state.X_test = np.array(self.test_set, dtype='object')
    elif isinstance(self.test_set, np.ndarray):
      self.state.X_test = self.state.test_set
    else:
      raise RuntimeError(f'Invalid test_set type, expected: list, str. Got {type(self.test_set)}.')

    self.state.X_test = pnorm.normalize(self.state.X_test, self.emojis, self.keywords)

  def segment(self):
    if self.char_level:
      self.state.X_test = pseg.segment_char(self.state.X_test)
    else:
      self.state.X_test = pseg.segment(self.state.X_test, 'vncorenlp', punct_replacer='<punct>', num_replacer='<number>')
    self.state.X_seg = self.state.X_test

  def tokenize(self):
    self.state.X_test = ptok.tokenize(self.state.X_test, self.tokenizer, maxlen=self.input_length)
    self.mask(0)

  def mask(self, mask_id):
    self.state.X_test_mask = np.not_equal(self.state.X_test, mask_id).astype('int32')

  def run(self):
    self.load()
    self.segment()
    self.tokenize()

    return self.state
