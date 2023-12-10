from django import template
from news.templatetags.censor_words import censor_tuple

register = template.Library()


@register.filter()
def censor_filter(cens_str: str) -> str:
    try:
        if not isinstance(cens_str, str):
            raise ValueError
        cens_str_low = cens_str.lower()
        for word in censor_tuple:
            if word in cens_str_low:
                word_v = f"{word[0]}{'*'*(len(word)-1)}"
                for _ in range(cens_str_low.count(word)):
                    word_i = cens_str_low.index(word)
                    word_cens_str = cens_str[word_i:(word_i+len(word))]
                    cens_str = cens_str.replace(word_cens_str, word_v)
                    cens_str_low = cens_str.lower()
    except ValueError:
        print('Censor filter is used with str obj!')
    return cens_str
