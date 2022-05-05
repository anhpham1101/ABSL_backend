# ===== Tokenization ===== #
import numpy as np

def pad_sequences(sequences, maxlen, truncating, padding):
  if maxlen is None:
    maxlen = max([sequence.shape[-1] for sequence in sequences])

  def exec(sequence):
    # Do padding
    sequence = np.array(sequence, dtype='int32')
    if sequence.shape[-1] < maxlen: 
      pads = np.zeros((maxlen - sequence.shape[-1]))
      if padding == 'post':
        return np.concatenate([sequence, pads])
      elif padding == 'pre':
        return np.concatenate([pads, sequence])
      else:
        raise RuntimeError('`padding` must be either `post` or `pre`')
    else:
      if truncating == 'post':
        return sequence[:maxlen]
      elif truncating == 'pre':
        return sequence[-maxlen::1]
      else:
        raise RuntimeError('`truncating` must be either `post` or `pre`')

  return np.array(list(map(exec, sequences)), dtype='int32')

def tokenize(texts, tokenizer, use_padding=True, maxlen=None, truncating='post', padding='post'):
  def trim_pad(text):
    start = text[0:1]
    end = text[-1:]
    content = text[1:-1]
    if maxlen is not None:
      content = content[:maxlen]

    return tokenizer.texts_to_sequences([start +  content + end])[0]
  
  # seq = np.vectorize(trim_pad, otypes=[object])(texts)
  seq = np.array(list(map(trim_pad, texts)), dtype='object')

  if not use_padding:
    return seq
  
  return pad_sequences(seq, maxlen=maxlen+2 if maxlen is not None else None,
                          truncating=truncating, padding=padding)
