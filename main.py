


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
    return convert_word_to_value(correct_guesses)


def word_guess_to_non_values(word, hints):
    incorrect_guesses = ''
    incorrect_values = list()
    for i in range(0,len(hints)):
        if hints[i].lower() == 'b':
            incorrect_guesses+=word[i]
            incorrect_values.append(convert_letter_to_prime(word[i]))

    return incorrect_values

def generate_string_location_map(all_availible_words):
    #create object so filling it is simple
    letter_spot_value_map = dict()
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        letter_spot_value_map[letter] = {0:set(), 1:set(), 2:set(), 3:set(), 4:set()}

    for word in all_availible_words:
        word = word.strip()
        value = convert_word_to_value(word)
        for index, letter in enumerate(word):
            letter_spot_value_map[letter][index].add(value)

    return letter_spot_value_map

def get_green_and_yellow_tuples(word, hints):
    yellows = list()
    greens = list()
    # print("guess", word, "response", hints)
    for i in range(0,len(hints)):
        if hints[i].lower() == 'y':
            yellows.append((word[i], i))
        if hints[i].lower() == 'g':
            greens.append((word[i], i))
    return greens, yellows


def let_us_play(all_words_value_to_word_map, letter_spot_value_map):
    print("now let's start")
    availible_word_values = set(all_words_value_to_word_map.keys())
    while len(availible_word_values) > 1:
        # print("we got there?", 9956969 in availible_word_values)
        guess = input("what word was guessed\n").lower()
        if len(guess) < 5:
            if guess == 's':
                for value in availible_word_values:
                    print(all_words_value_to_word_map[value])
                continue
            if guess == 'q':
                return 'q'
            if guess == 'r':
                return 'r'
        response = input("what did the system respond. b for blank, y for yellow, g for green\n").lower()

        for word_value in set(availible_word_values):
            correct_value = word_guess_to_value(guess, response)
            # if word_value == '9956969':
                # print('correct value', correct_value)
                # print(9956969 & correct_value)
            if word_value % correct_value != 0:
                availible_word_values.remove(word_value)
            for incorrect_value in word_guess_to_non_values(guess, response):
                if word_value not in availible_word_values:
                    break
                if word_value % incorrect_value == 0:
                    availible_word_values.remove(word_value)

        # print("we got there?", 9956969 in availible_word_values)
        greens, yellows = get_green_and_yellow_tuples(guess, response)
        # print('greens and yellows', greens, yellows)

        for letter, index in greens:
            availible_word_values = availible_word_values.intersection(letter_spot_value_map[letter][index])

        for letter,index in yellows:
            availible_word_values = availible_word_values.difference(letter_spot_value_map[letter][index])

        # print("we got there?", 9956969 in availible_word_values)
        print("availible words left", len(availible_word_values))
        if len(availible_word_values) < 11:
            for value in availible_word_values:
                print(all_words_value_to_word_map[value])


    if len(availible_word_values) == 0:
        print('seems like we hit an error quitting')
        return 'q'
    print("the word is", all_words_value_to_word_map[availible_word_values.pop()])
    return 'r'


if __name__ == '__main__':
    all_words = get_all_words()
    print('there', convert_word_to_value('there'))
    print("Menu instead of guessing a word type these letters\nclick enter for next guess\n\ts to show what words are availilbe\n\tq to quit\n\tr to restart with a new word\n")
    while (let_us_play(generate_numbers_to_words_map(all_words), generate_string_location_map(all_words)) == 'r'):
        pass
