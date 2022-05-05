import os, sys
import string
import numpy as np 

cur_dir = os.path.abspath(__file__)
cur_dir = os.path.dirname(cur_dir)

# ===== Segmentation ===== #
class WordSegmenter:
  from vncorenlp import VnCoreNLP as __VnCoreNLP
  VnCoreNLPTokenizer = __VnCoreNLP(f'{cur_dir}/../segmenter/vncorenlp/VnCoreNLP-1.1.1.jar', annotators='wseg', max_heap_size='-Xmx500m')#max_heap_size='-Xmx2g')

  def tokenize(segmenter, texts, punct_replacer=None, num_replacer=None):
    def get_pairs(lst):
      for i in range(len(lst)):
        cur = lst[i]
        next_ = lst[i+1] if i != len(lst) - 1 else None 
        yield (cur, next_)

    def exec(text):
      text = str(text)
      if segmenter == 'vncorenlp':
        from functools import reduce
        try:
          segments = WordSegmenter.VnCoreNLPTokenizer.tokenize(text)
        except:
          WordSegmenter.VnCoreNLPTokenizer.close()
          WordSegmenter.VnCoreNLPTokenizer = WordSegmenter.__VnCoreNLP(f'{cur_dir}/../segmenter/vncorenlp/VnCoreNLP-1.1.1.jar', annotators='wseg', max_heap_size='-Xmx500m')#max_heap_size='-Xmx2g')
          segments = WordSegmenter.VnCoreNLPTokenizer.tokenize(text)
        segments = list(reduce(lambda lst, seg: lst + seg, segments, []))
        segments = ['<s>'] + list(reduce(
          lambda seg, pair_tok: seg + replace(pair_tok, punct_replacer, num_replacer),
          get_pairs(segments), [])) + ['</s>']

        # segments = ['<s>'] + [replace(pair_tok, punct_replacer, num_replacer) for pair_tok in get_pairs(segments)] + ['</s>']
      return segments
    # return np.array(list(map(exec, texts)), dtype=object)
    return list(map(exec, texts))

def replace(pair_tok, punct_replacer=None, num_replacer=None):
  tok, next_tok = pair_tok
  tok = tok.replace('-', '_')

  if tok == '%':
    return []
  if tok in string.punctuation:
    return [punct_replacer if punct_replacer is not None else tok]
  if tok.isdigit():
    if next_tok not in ['%', 'ngày', 'hôm']:
      return [num_replacer if num_replacer is not None else tok]
    if next_tok == '%':
      num = int(tok)
      if num >= 97:
        return ['100%']
      return [f'{str(num//10*10)}%']
  return [tok]

def segment(texts, segmenter, punct_replacer=None, num_replacer=None):
  # texts = pre_segment(texts, emojis, keywords)
  texts = WordSegmenter.tokenize(segmenter, texts, punct_replacer, num_replacer)
  return texts

def segment_char(texts):
  def exec(text):
    return ['<s>'] + [replace(char) for char in text] + ['</s>']

  def replace(char):
    if char == ' ':
      return '<space>'
    elif char == '.':
      return '<punct>'
    elif char.isdigit():
      return '<number>'
    else:
      return char 

  return list(map(exec, texts))
  