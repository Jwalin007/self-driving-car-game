from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

ps = PorterStemmer()
file_content = open('dataset/data1.txt').read()
# Toeknization
tokens = word_tokenize(file_content)

stop_words = set(stopwords.words('english'))

# filtered_sentence = [w for w in tokens if not w in stop_words]

filtered_sentence = []

# Sopwords removal
for w in tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

stemmed = []

# Stemming
for w in filtered_sentence:
    stemmed.append(ps.stem(w).lower())

freq = {}
# Calculation word Frequency
for word in stemmed:
    if freq.has_key(word):
        freq[word] += 1
    else:
        freq[word] = 1

print(freq)

# Sepration of words form [words: frequency] to [words]
wordsdict = {}
for w in freq:
    wordsdict[w] = freq[w]

# lower max_font_size
wordcloud = WordCloud(max_font_size=40).generate(file_content)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

plt.bar(range(len(wordsdict)), wordsdict.values(), align='center')
plt.xticks(range(len(wordsdict)), wordsdict.keys())
plt.show()




