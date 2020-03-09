def to_eu_dic():
    word_and_context_pairs = {}
    with open('/Users/fniu/kindle/kindleWords.txt', 'r') as in_file:
        for in_file_line in in_file:
            in_file_line_split = in_file_line.split("|")
            word_and_context_pairs[in_file_line_split[0]] = in_file_line_split[
                1]
    with open('/Users/fniu/kindle/eudic.csv', 'w') as out_file:
        for word, context in word_and_context_pairs.items():
            trimmed_context = context\
                .replace("’", "'")\
                .replace(" ", " ")\
                .replace("—", " ")\
                .replace("“", "\"")\
                .replace("\n", " ")
            out_file.write(word + "," + trimmed_context + "\n")


if __name__ == "__main__":
    to_eu_dic()
