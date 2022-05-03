from textblob import TextBlob

def hello(name):
    output = f'Hello {name}'
    return output

def extract_sentiment(text):
    text = TextBlob(text)

    return text.sentiment.polarity

def text_contain_word(word: str, text: str):
    return word in text


def bubble(tab):
    n = len(tab)
    tab1 = tab[:]
    for i in range(n - 1):
        for j in range(n - i - 1):
            if tab1[j] > tab1[j + 1]:
                tab1[j], tab1[j + 1] = tab1[j + 1], tab1[j]
    return tab1