#!/usr/bin/python

import datetime
import shutil
import sqlite3


def copy_db(kindle_db_path):
    current_datetime = datetime.datetime.now()
    date_suffix = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    backup_db_path = r"/Users/fniu/kindle/kindleconverter/dbs/vocab_{}.db".format(
        date_suffix)
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


def to_eudic(word_and_context_pairs):
    eudic_file_path = r"/Users/fniu/kindle/eudic.csv"
    with open(eudic_file_path, 'w') as out_file:
        for word, context in word_and_context_pairs.items():
            trimmed_context = context\
                .replace("’", "'")\
                .replace(" ", " ")\
                .replace("—", " ")\
                .replace("“", "\"")\
                .replace("\n", " ")
            out_file.write(word + "," + trimmed_context + "\n")
    print("Wrote csv file at {}".format(eudic_file_path))


def main():
    kindle_db_path = r"/Volumes/Kindle/system/vocabulary/vocab.db"

    backup_db_path = copy_db(kindle_db_path)
    word_and_context_pairs = read_db(backup_db_path)
    to_eudic(word_and_context_pairs)


if __name__ == "__main__":
    main()
