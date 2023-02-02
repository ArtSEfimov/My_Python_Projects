import collections
import random

alphabet = '''а б в г д е ж з
и й к л м н о п
р с т у ф х ц ч
ш щ ъ ы ь э ю я'''


class Word:

    def __init__(self, user_word):
        user_word = user_word.lower().replace('ё', 'е')
        if self.__check_user_word(user_word):
            self.user_word = user_word
        else:
            raise AttributeError(f'слово должно состоять из букв алфавита:\n{"".join(a.upper() for a in alphabet)}')

    @staticmethod
    def __check_user_word(user_word):
        return all(
            map(
                lambda x: x in alphabet, user_word
            )
        )


class Game:
    __WORDS = [
        'амбар', 'кегля', 'камыш', 'город', 'товар', 'буква', 'успех',
        'замок', 'маска', 'шапка', 'пират', 'ответ', 'тариф', 'взнос',
        'хомяк', 'жизнь', 'мумия', 'жокей', 'циник', 'устье', 'обмен',
        'лимон', 'хомяк', 'хакер', 'диета', 'балет', 'такси', 'замок',
        'арбуз', 'алмаз', 'налог', 'слава', 'грамм', 'трата', 'танго',
        'жизнь', 'лилия', 'полис', 'акция', 'игрок', 'батон', 'абзац',
        'алмаз', 'ткань', 'какао', 'макет', 'эмаль', 'афиша', 'архив',
        'зачет', 'довод', 'рожок', 'устой', 'салют', 'рубль', 'лидер',
        'вклад', 'полюс', 'вагон', 'лимит', 'доход', 'повар', 'юноша',
        'уклад', 'актив', 'чашка', 'экран', 'проза', 'сумма', 'биржа',
        'закон', 'олень', 'идеал', 'место', 'егерь', 'муляж', 'ведро',
        'уклон', 'алиби', 'билет', 'дрель', 'тыква', 'аванс',
        'упрек', 'юрист', 'балет', 'лавка', 'химия', 'вечер'
    ]

    def __init__(self):
        self.words = []
        random.shuffle(self.__WORDS)
        self.__secret_word = random.choice(self.__WORDS)
        self.alphabet = alphabet
        self.win = False

    @staticmethod
    def two_words(first_word, second_word):
        dict_word = collections.Counter(first_word)

        def dict_func(letter):
            dict_word[letter] = dict_word.get(letter, 0) - 1
            if dict_word.get(letter) < 0:
                del dict_word[letter]
            return letter in dict_word

        word = ''.join(
            [letters[0].upper()
             if letters[0] == letters[1] else letters[0]
             for letters in zip(second_word, first_word)]
        )

        tmp_word = [None for _ in range(5)]
        if not word.islower():
            for i in range(5):
                if word[i].isupper() and word[i].lower() in first_word:
                    tmp_word[i] = word[i]
                    dict_func(second_word[i].lower())

        for i in range(5):
            if word[i] in first_word and dict_func(second_word[i].lower()):
                tmp_word[i] = word[i]

        word = ''.join(
            [
                letter
                if letter else '*'
                for letter in tmp_word
            ]
        )

        return word

    def update_alphabet(self, user_word, new_word):
        letters = [letter[0]
                   for letter in zip(user_word, new_word)
                   if letter[1] == '*'
                   ]
        for letter in letters:
            self.alphabet = self.alphabet.replace(letter, '*')
        for letter in [letter.lower()
                       for letter in new_word
                       if letter.isalpha()]:
            self.alphabet = self.alphabet.replace(letter, letter.upper())

    def add_word(self, word: Word):
        validator = self.__valid_word(word.user_word)
        if validator[0]:
            if word.user_word == self.__secret_word:
                self.win = True

            new_word = self.two_words(self.__secret_word, word.user_word)
            self.update_alphabet(word.user_word, new_word)
            self.words.append(new_word)
            return validator
        return validator

    def __valid_word(self, word):
        if len(word) != 5:
            return False, 'length'
        if word not in self.__WORDS:
            return False, 'contain'
        return True,

    def play(self):
        print('Let`s play the game')
        print()
        count = 1
        while True:
            print()
            addition = self.add_word(Word(input('your word: ')))
            if addition[0]:
                print(
                    '\n'.join(self.words)
                )
                if self.win:
                    print()
                    print('YOU HAVE WON!!!')
                    print()
                    print(f'{count}/6 attempts')
                    break
                else:
                    print()
                    print(self.alphabet)
                    print()
                    print(f'{6 - count} attempts left')
                count += 1
            else:
                error_description = addition[1]
                if error_description == 'length':
                    print('incorrect word length, try again')
                    continue
                elif error_description == 'contain':
                    print('nonexistent word, try again')
                    continue
            if count > 6:
                print(
                    '\n'.join(self.words)
                )

                if self.win:
                    print()
                    print('THE GAME IS OVER')
                    print('YOU HAVE WON!!!')
                    print()
                    print(f'6/6 attempts')
                else:
                    print()
                    print('THE GAME IS OVER')
                    print(f'6/6 attempts')
                    print()
                    print(f'we made a word {self.__secret_word.upper()}')
                break


new_game = Game()

new_game.play()
