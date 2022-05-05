import regex as re
import unicodedata

REGEX_SPECIAL = u'*^$*+?!#|\\()[].'
REGEX_SPECIAL_TRANSLATOR = str.maketrans({ch: f'\\{ch}' for ch in REGEX_SPECIAL})

def len_reg(r):
  return len(r[r.find('>') + 1:])

def mutate_keyword(word):
  from preprocessing.preprocess.utils import remove_accents
  word = unicodedata.normalize('NFKC', word)
  word = word.translate(REGEX_SPECIAL_TRANSLATOR)
  non_accent_word = remove_accents(word)
  return list(set([
           word, 
           non_accent_word, 
           ''.join(word.split()), 
           ''.join(non_accent_word.split())
      ]))

def make_regex_from_word_list(k, lst, mutation=None): 
  if mutation is not None:
    lst_mutate = list(set([word for sublist in list(map(mutation, lst)) for word in sublist]))
  else:
    lst_mutate = lst[0:]
  lst_mutate = sorted(lst_mutate, key=len, reverse=True)
  regexps = [fr'(?P<{k}>(?<!\w){el}(?!\w))' for el in lst_mutate]
  return regexps
  
def substitute_gen(group_words, mutation):
  # token_spec = [(k.replace('-', '_'), make_regex_from_word_list(v, mutation)) for k,v in group_words.items()]
  # tok_regex = '|'.join(f'(?P<{k}>{v})' for k,v in token_spec)
  tok_regex = [r for k,v in group_words.items() for r in make_regex_from_word_list(k.replace('-', '_'), v[1], mutation)]
  tok_regex = sorted(tok_regex, key=len_reg, reverse=True)
  tok_regex = '|'.join(tok_regex)
  r = re.compile(fr'{tok_regex}', flags=re.U|re.I)
  
  def exec(text):
    text = str(text)
    text = r.sub(lambda m: ' ' + group_words[m.lastgroup.replace('_', '-')][0] + ' ', text)
    return text
  return exec
  