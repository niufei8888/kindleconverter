#!/usr/bin/env python

import re
import sqlite3

from nltk.stem.wordnet import WordNetLemmatizer


def read_db(kindle_db_path):
    print("Will read vocab.db from {}..".format(kindle_db_path))

    conn = sqlite3.connect(kindle_db_path)

    word_and_context_pairs = {}
    with conn:
        cursor = conn.execute(
            "SELECT word, usage FROM "
            "WORDS INNER JOIN LOOKUPS WHERE LOOKUPS.word_key=WORDS.id "
            "AND category = 0;"
        )
        for row in cursor:
            word_and_context_pairs[row[0]] = row[1]

    print("Reading DB done.")
    return word_and_context_pairs


# try shifting the tense to present or falling back to original form
def normalize_word(wordnet_lemmatizer, word):
    normalized_word = wordnet_lemmatizer.lemmatize(word, 'v')
    if normalized_word and normalized_word != word:
        return normalized_word

    normalized_word = wordnet_lemmatizer.lemmatize(word, 'n')
    if normalized_word and normalized_word != word:
        return normalized_word

    return word


def to_eudic_csv(word_and_context_pairs, date_suffix):
    eudic_file_path = r"/Users/fniu/kindle/kindleconverter/csvs" \
                      r"/vocab_{}_raw.csv".format(date_suffix)
    wordnet_lemmatizer = WordNetLemmatizer()
    word_and_context_map = {}
    for word, context in word_and_context_pairs.items():
        trimmed_word = word.strip().lower()
        normalized_word = normalize_word(wordnet_lemmatizer, trimmed_word)

        trimmed_context = context \
            .replace("’", "'") \
            .replace(" ", " ") \
            .replace("—", " ") \
            .replace("“", "'") \
            .replace("”", "'") \
            .replace("\"", "'") \
            .replace("\n", " ")

        if normalized_word in word_and_context_map:
            previous_context = word_and_context_map[normalized_word]
            new_context = previous_context + trimmed_context
            word_and_context_map[normalized_word] = new_context
        else:
            word_and_context_map[normalized_word] = trimmed_context

    with open(eudic_file_path, 'w') as out_file:
        for k, v in word_and_context_map.items():
            out_file.write(k + "," + v + "\n")
    print("Wrote csv file at {}".format(eudic_file_path))
    return eudic_file_path


def main():
    backup_db_path = \
        "/Users/fniu/kindle/kindleconverter/dbs/vocab_2020-05-25_15-45-05.db"
    match = re.search(
        r"/Users/fniu/kindle/kindleconverter/dbs/vocab_([\w-]+)\.db",
        backup_db_path)
    time_string = match.group(1)
    if not time_string:
        raise Exception("Not able to parse datetime from " + backup_db_path)
    word_and_context_pairs = read_db(backup_db_path)
    to_eudic_csv(word_and_context_pairs, time_string)


if __name__ == "__main__":
    # NLKT https://www.nltk.org/data.html
    # env variable required: NLTK_DATA=/Users/fniu/kindle/nltk_data
    main()
