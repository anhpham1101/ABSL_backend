import emoji
import regex as re
import itertools
import unicodedata
import string
import numpy as np
import preprocessing.preprocess.substitution as psubs

EMO_ABBREVS = {
    'smile': ('🙂', ['\\)', '\\]', '}']),
    'sad': ('🙁', ['\\(', '\\[', '{']),
    'pacman': ('🤣', ['vV'])
}
EMO_EYES = [':', '=', ':-', '=-', ":'", "='", ":'-", "='-", ":-'", "=-'"]

def make_emo_abbrev_regex(emo_abbrevs, emo_eyes):
  r = []
  for emo, patterns in emo_abbrevs.items():
    for pattern in patterns[1]:
      for eye in emo_eyes:
        r += [fr'(?P<{emo}>{eye}[{pattern}][{pattern}]*)']

  r = '|'.join(r)
  return r

def transform_emo_abbrev(emo_abbrevs, emo_eyes, text):
  r = re.compile(make_emo_abbrev_regex(emo_abbrevs, emo_eyes))
  text = r.sub(lambda m: emo_abbrevs[m.lastgroup][0], text)
  return text

def separate_emoji(text):
  emoji_reg = emoji.get_emoji_regexp()
  # return emoji_reg.sub(' ', text)
  return emoji.replace_emoji(text, replace=' ')
  #return list(map(exec, texts))

def separate_dot(text):
  dot_re = re.compile(r"(\.+)")
  #def exec(text):
  return re.sub(dot_re, r' . ', str(text))
  #return list(map(exec, texts))

def convert_utf8(text):
  return unicodedata.normalize('NFKC', text)


PUNCTUATION = set('.?!,;:_')
PERCENT = set('%')
SPECIAL_CHARS  = set(string.punctuation) - PUNCTUATION - PERCENT

def strip_repetitive_punctuations(text):
  temp = []
  for k,v in itertools.groupby(text):
    if k in set.union(PUNCTUATION, PERCENT):
      temp.append(k)
    # elif k in PERCENT:
    #   temp.append(k)
    elif k in SPECIAL_CHARS:
      temp.append(' ')
    elif k.isdigit():
      temp.extend(v)
    else:
      temp.append(k)
      # And may do some further stuffs :D 

  return ''.join(temp)

def strip_repetitive_emojis(text):
  temp = []
  for k,v in itertools.groupby(text.split()):
    if emoji.is_emoji(k):
      temp.append(k)
    else:
      temp.extend(v)
  return ' '.join(temp)

def normalize(texts, emojis=None, keywords=None):
  if emojis is not None:
    emo_substitute = psubs.substitute_gen(emojis, None)
  if keywords is not None:
    keywords_substitute = psubs.substitute_gen(keywords, psubs.mutate_keyword)

  # emoji_reg = emoji.get_emoji_regexp()

  def exec(text):
    text = str(text)
    text = text.replace('\n', '.')
    text = text.replace('\r', '.')
    text = separate_emoji(text)
    text = separate_dot(text)
    text = convert_utf8(text)
    text = transform_emo_abbrev(EMO_ABBREVS, EMO_EYES, text)
    text = strip_repetitive_emojis(text)
    # Mapping emojis, keywords to its representative
    if emojis is not None:
      text = emo_substitute(text)
    if keywords is not None:
      text = keywords_substitute(text)
    # Remove all emojis that not appear in keywords
    text = emoji.replace_emoji(text, replace='')
    # You may not want to strip all punctuation
    text = strip_repetitive_punctuations(text)
    text = ' '.join(text.split())
    text = text.lower().replace('_', '-')
      
    return text
  return np.array(list(map(exec, texts)), dtype='object')
