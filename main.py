


def get_all_words():
    all_words_file = open("dictionary.txt", "rt")
    all_words = all_words_file.readlines()
    return all_words


first_26_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]

def convert_letter_to_prime(letter):
    return first_26_primes[ord(letter)-97]


def convert_word_to_value(word):
    value = 1
    for letter in word.strip():
        value*=convert_letter_to_prime(letter)
    return value

def generate_numbers_to_words_map(words):
    numbers_to_words_map = dict()

    for word in words:
        numbers_to_words_map[convert_word_to_value(word)]=word.strip()

    return numbers_to_words_map


def word_guess_to_value(word, hints):
    correct_guesses = ''
    for i in range(0,len(hints)):
        if hints[i].lower() == 'y':
            correct_guesses+=word[i]
        if hints[i].lower() == 'g':
            correct_guesses+=word[i]
        # print(i, hints[i], word[i], correct_guesses)
    # print(correct_guesses)
    return convert_word_to_value(correct_guesses)


def word_guess_to_non_values(word, hints):
    incorrect_guesses = ''
    incorrect_values = list()
    for i in range(0,len(hints)):
        if hints[i].lower() == 'b':
            incorrect_guesses+=word[i]
            incorrect_values.append(convert_letter_to_prime(word[i]))

    return incorrect_values


if __name__ == '__main__':
    # some_words = {55737073: 'windy', 85822913: 'wiser', 657549323: 'wispy', 12876205: 'witch', 933457093: 'witty', 57200363: 'woken', 13754926: 'woman', 75652093: 'women', 124492613: 'woody', 123025837: 'wooer', 658032383: 'wooly', 1796250559: 'woozy', 61631899: 'world', 1408015237: 'worry', 1131980477: 'worst', 73756207: 'would', 85716673: 'wound', 145768667: 'woven', 1569530: 'wrack', 13659974: 'wrath', 3452966: 'wreak', 8632415: 'wreck', 264931601: 'wrest', 85124219: 'wring', 553947893: 'wrist', 90946669: 'write', 270176869: 'wrung', 1762597379: 'wryly', 1308530: 'yacht', 5597482: 'yearn', 10151438: 'yeast', 6356119: 'yield', 243281917: 'young', 448956643: 'youth', 406626: 'zebra', 512647619: 'zesty', 15104954: 'zonal'}

    # all_words_value_to_word_map = some_words
    all_words_value_to_word_map = generate_numbers_to_words_map(get_all_words())

    # print(all_words_value_to_word_map)
    availible_word_values = list(all_words_value_to_word_map.keys())
    # print(availible_word_values)
    while len(availible_word_values) != 1:
        guess = input("what word was guessed\n")
        response = input("what did the system respond. b for blank, y for yellow, g for green\n")

        for word_value in list(availible_word_values):
            correct_value = word_guess_to_value(guess, response)
            if word_value % correct_value != 0:
                availible_word_values.remove(word_value)
            for incorrect_value in word_guess_to_non_values(guess, response):
                if word_value not in availible_word_values:
                    break
                if word_value % incorrect_value == 0:
                    availible_word_values.remove(word_value)

        print("availible words", len(availible_word_values))
        if len(availible_word_values) < 11:
            for value in availible_word_values:
                print(all_words_value_to_word_map[value])

    print("the word is", all_words_value_to_word_map[availible_word_values[0]])
