from AvailibleWords import AvailibleWords
from WordleGameEngine import WorldeGameEngine

import statistics

def get_all_words():
    all_words_file = open("dictionary.txt", "rt")
    all_words = all_words_file.readlines()
    return [word.strip().lower() for word in all_words]

def let_us_play(all_words):
    availible_words = AvailibleWords(all_words)
    print("now let's start")
    while len(availible_words) > 1:
        guess = input("what word was guessed\n").strip().lower()
        if len(guess) < 5:
            if guess == 's':
                for words in availible_words.words():
                    print(word)
                continue
            if guess == 'q':
                return 'q'
            if guess == 'r':
                return 'r'
        response = input("what did the system respond. b for blank, y for yellow, g for green\n").lower().strip()

        availible_words.filter_guess(guess, response)
        availible_words.words()
        no_words_left = len(availible_words)
        print("availible words left", no_words_left)
        if no_words_left < 11:
            for word in availible_words.words():
                print(word)


    if len(availible_words) == 0:
        print('seems like we hit an error exiting program')
        return 'q'
    print("the word is", availible_words.words().pop())
    return 'r'


def human_against_gameEngine(all_words):
    gameEngine = WorldeGameEngine(all_words)
    word=input("would you like to set the word\n").strip()
    if word not in all_words:
        print("invalid word setting a random one")
        word=None
    gameEngine.set_word_to_guess(word)
    response = ''
    while(response != 'ggggg'):
        guess = input("what would would you like to guess\n")
        response = gameEngine.guess(guess)
        print("response was", response)


def assistant_mode(all_words):
    availible_words = AvailibleWords(all_words)
    print("Menu instead of guessing a word type these letters\nclick enter for next guess\n\ts to show what words are availilbe\n\tq to quit\n\tr to restart with a new word\n")
    while (let_us_play(all_words) == 'r'):
        pass


def self_playing_machine(all_words):
    availible_words = AvailibleWords(all_words)
    gameEngine = WorldeGameEngine(all_words)
    gameEngine.set_word_to_guess()
    response = ''
    round = 0
    while(response != 'ggggg'):
        if round % 20 == 0 and round != 0:
            input("We just reached %s guesses do you want to continue?" % (round))
        print("Words left in the pool", len(availible_words))
        if len(availible_words) == 0:
            print(gameEngine.guesses_so_far, gameEngine.secret_word)
        guess = availible_words.get_next_guess()
        # print("guess was", guess)
        response = gameEngine.guess(guess)
        # print("response was", response)
        availible_words.filter_guess(guess, response)
        round+=1

    return gameEngine.guesses_so_far

if __name__ == '__main__':
    all_words = get_all_words()

    # human_against_gameEngine(all_words)
    assistant_mode(all_words)
    # guesses_distribution = set()
    # total_games = 200
    # for count in range(total_games):
    #     guesses = self_playing_machine(all_words)
    #     # print(guesses)
    #     guesses_distribution.add(len(guesses))
    #
    # print(statistics.mean(guesses_distribution))
