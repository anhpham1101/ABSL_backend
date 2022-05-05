import pandas as pd
import numpy as np
# from preprocess.normalizing import normalize
# from preprocess.augmenting import add_remove_accent_texts
# from preprocess.preparation import WordSegmenter

def csv_to_dataset(filename, content_name, label_name=''):
  ds = pd.read_csv(filename).fillna(0)
  X = ds.iloc[:][content_name].values
  y = ds.iloc[:][label_name].values.astype('int32').transpose() if label_name != '' else []
  
  return X.astype('object'), y

def remove_accents(text):
  s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
  s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
  s = ''
  for c in text:
    if c in s1:
      s += s0[s1.index(c)]
    else:
      s += c
  return s
  