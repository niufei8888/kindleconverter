#!/usr/bin/python

import datetime
import shutil


def copy_db(kindle_db_path, date_suffix):
    backup_db_path = r"/Users/fniu/kindle/kindleconverter/dbs/vocab_{}.db" \
        .format(date_suffix)
    print("Will back up Kindle DB at {} to {} ..".format(kindle_db_path,
                                                         backup_db_path))
    shutil.copyfile(kindle_db_path, backup_db_path)
    print("Backed up at {}".format(backup_db_path))


def main():
    kindle_db_path = r"/Volumes/Kindle/system/vocabulary/vocab.db"
    current_datetime = datetime.datetime.now()
    date_suffix = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    print("date_suffix={}".format(date_suffix))

    copy_db(kindle_db_path, date_suffix)


if __name__ == "__main__":
    main()
