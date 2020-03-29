#!/usr/bin/env python

import sqlite3

import datetime
import shutil
from nltk.stem.wordnet import WordNetLemmatizer


def copy_db(kindle_db_path, date_suffix):
    backup_db_path = r"/Users/fniu/kindle/kindleconverter/dbs/vocab_{}.db" \
        .format(date_suffix)
    print("Will back up Kindle DB at {} to {} ..".format(kindle_db_path,
                                                         backup_db_path))
    shutil.copyfile(kindle_db_path, backup_db_path)
    print("Backed up at {} .".format(backup_db_path))
    return backup_db_path


def read_db(kindle_db_path):
    print("Will read vocab.db from {}..".format(kindle_db_path))

    conn = sqlite3.connect(kindle_db_path)

    word_and_context_pairs = {}
    with conn:
        cursor = conn.execute(
            "SELECT word, usage from "
            "WORDS INNER JOIN LOOKUPS where LOOKUPS.word_key=WORDS.id;"
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
    eudic_file_path = r"/Users/fniu/kindle/kindleconverter/csvs/vocab_{}.csv" \
        .format(date_suffix)
    wordnet_lemmatizer = WordNetLemmatizer()
    with open(eudic_file_path, 'w') as out_file:
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

            out_file.write(normalized_word + "," + trimmed_context + "\n")
    print("Wrote csv file at {}".format(eudic_file_path))
    return eudic_file_path


def main():
    kindle_db_path = r"/Volumes/Kindle/system/vocabulary/vocab.db"
    current_datetime = datetime.datetime.now()
    date_suffix = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    print("date_suffix={}".format(date_suffix))

    backup_db_path = copy_db(kindle_db_path, date_suffix)
    # date_suffix = r"2020-03-28_11-35-38"
    # backup_db_path = r"/Users/fniu/kindle/kindleconverter/dbs/vocab_{}.db"\
    #     .format(date_suffix)

    word_and_context_pairs = read_db(backup_db_path)
    to_eudic_csv(word_and_context_pairs, date_suffix)


if __name__ == "__main__":
    # NLKT https://www.nltk.org/data.html
    # env variable required: NLTK_DATA=/Users/fniu/kindle/nltk_data
    main()
