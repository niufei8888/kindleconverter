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


def to_eudic_csv(word_and_context_pairs, date_suffix):
    eudic_file_path = r"/Users/fniu/kindle/kindleconverter/csvs/" \
                      r"vocab_{}_with_tense.csv" \
        .format(date_suffix)
    with open(eudic_file_path, 'w') as out_file:
        for word, context in word_and_context_pairs.items():
            trimmed_context = context \
                .replace("’", "'") \
                .replace(" ", " ") \
                .replace("—", " ") \
                .replace("“", "\"") \
                .replace("”", "\"") \
                .replace("\n", " ")
            out_file.write(word + "," + trimmed_context + "\n")
    print("Wrote csv file at {}".format(eudic_file_path))
    return eudic_file_path


def remove_tense(eudic_file_path, date_suffix):
    csv_without_tense = r"/Users/fniu/kindle/kindleconverter/csvs/" \
                        r"vocab_{}.csv" \
        .format(date_suffix)
    wordnet_lemmatizer = WordNetLemmatizer()
    with open(csv_without_tense, 'w') as out_file:
        with open(eudic_file_path, 'r') as in_file:
            for line in in_file.readlines():
                first_comma_index = line.index(",")
                word = line[0:first_comma_index]
                context = line[first_comma_index:-1]
                word_to_write = wordnet_lemmatizer.lemmatize(word, 'v')
                if not word_to_write:
                    word_to_write = word
                out_file.write(word_to_write + "," + context + "\n")
    print("Written  csv without tense at {} .".format(csv_without_tense))


def main():
    kindle_db_path = r"/Volumes/Kindle/system/vocabulary/vocab.db"
    current_datetime = datetime.datetime.now()
    date_suffix = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    print("date_suffix={}".format(date_suffix))

    backup_db_path = copy_db(kindle_db_path, date_suffix)
    word_and_context_pairs = read_db(backup_db_path)
    eudic_file_path = to_eudic_csv(word_and_context_pairs, date_suffix)
    remove_tense(eudic_file_path, date_suffix)


if __name__ == "__main__":
    # NLKT https://www.nltk.org/data.html
    # env variable required: NLTK_DATA=/Users/fniu/kindle/nltk_data
    main()
