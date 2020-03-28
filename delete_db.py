#!/usr/bin/python

import sqlite3


def reset_kindle_db(kindle_db_path):
    print("Will reset Kindle DB..")

    conn = sqlite3.connect(kindle_db_path)

    with conn:
        conn.execute("DELETE FROM WORDS;")
        conn.execute("DELETE FROM LOOKUPS;")
        conn.commit()

    print("Resetting Kindle DB done.")


def main():
    kindle_db_path = r"/Volumes/Kindle/system/vocabulary/vocab.db"
    reset_kindle_db(kindle_db_path)


if __name__ == "__main__":
    main()
