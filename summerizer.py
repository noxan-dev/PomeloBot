from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from re import sub
import heapq


def nlp_parse(data):
    file_data = sub(r'\[[0-9]*]', ' ', data)
    file_data = sub(r'\s+', ' ', file_data)

    formatted_file_data = sub('[^a-zA-Z]', ' ', file_data)
    formatted_file_data = sub(r'\s+', ' ', formatted_file_data)

    sentence_list = sent_tokenize(file_data)

    stop_words = stopwords.words('english')

    word_frequencies = {}

    for word in word_tokenize(formatted_file_data):
        if word not in stop_words:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word] / maximum_frequency

    sentence_score = {}

    for sentence in sentence_list:
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_score.keys():
                        sentence_score[sentence] = word_frequencies[word]
                    else:
                        sentence_score[sentence] += word_frequencies[word]

    summary_sentence = heapq.nlargest(7, sentence_score, key=sentence_score.get)

    summary = ' '.join(summary_sentence)

    with open('parsed.txt', 'w', encoding='utf-8') as file:
        file.write(summary)
