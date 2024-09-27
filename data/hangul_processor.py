import unicodedata

class HangulProcessor:
    def __init__(self):
        pass

    def decompose_hangul_char(self, char):
        # 한글 문자 분해
        if '가' <= char <= '힣':
            base_code = ord(char) - 0xAC00
            choseong = base_code // 588
            jungseong = (base_code % 588) // 28

            # ㅔ/ㅐ 통합
            if jungseong == 1:
                jungseong = 5

            # 이중모음 분리
            w_diphthong = {9: 0, 14: 4, 10: 5, 15: 5, 11: 5, 16: 20}
            j_diphthong = {2: 0, 6: 4, 12: 8, 17: 13}
            diph = None

            if jungseong in w_diphthong:
                diph = 'w'
                jungseong = w_diphthong[jungseong]
            elif jungseong in j_diphthong:
                diph = 'j'
                jungseong = j_diphthong[jungseong]

            jongseong = base_code % 28

            if diph:
                return (
                    chr(0x1100 + choseong),
                    diph, chr(0x1161 + jungseong),
                    chr(0x11A7 + jongseong) if jongseong != 0 else ''
                )

            return (
                chr(0x1100 + choseong),
                chr(0x1161 + jungseong),
                chr(0x11A7 + jongseong) if jongseong != 0 else ''
            )
        else:
            return char

    def decompose(self, word):
        decomposed = [self.decompose_hangul_char(char) for char in word]
        return ''.join([part for char in decomposed for part in char if part != 'ᄋ'])

    def insert_ieung_if_two_vowels_in_a_row(self, word):
        result = []
        prev_is_vowel = False
        prev_is_None = True
        for char in word:
            if 'ᅡ' <= char <= 'ᅵ':  # 한글 중성(모음)의 범위
                if prev_is_vowel or prev_is_None:
                    result.append('ᄋ')  # 이전에 모음이 있었다면 ᄋ을 삽입
                prev_is_vowel = True
            else:
                prev_is_vowel = False
            prev_is_None = False
            result.append(char)
        return ''.join(result)

    def recompose_diphthongs(self, word):
        w_diphthong_reverse = {'ᅡ': 'ᅪ', 'ᅥ': 'ᅯ', 'ᅦ': 'ᅰ', 'ᅵ': 'ᅱ'}
        j_diphthong_reverse = {'ᅡ': 'ᅣ', 'ᅥ': 'ᅧ', 'ᅩ': 'ᅭ', 'ᅮ': 'ᅲ'}
        try:
            if 'w' in word:
                ind = word.index('w')
                word = list(word)
                word.insert(ind + 1, w_diphthong_reverse[word[ind + 1]])
                word.pop(ind + 2)
                word.remove('w')
                word = ''.join(word)
            elif 'j' in word:
                ind = word.index('j')
                word = list(word)
                word.insert(ind, j_diphthong_reverse[word[ind + 1]])
                word.pop(ind + 2)
                word.remove('j')
                word = ''.join(word)
        except KeyError:
            return None
        return word

    def compose(self, word):
        word = self.recompose_diphthongs(word)
        if word is None:
            return None
        normalized_word = unicodedata.normalize('NFD', word)
        processed_word = self.insert_ieung_if_two_vowels_in_a_row(normalized_word)
        return unicodedata.normalize('NFC', processed_word)

    def is_correctly_composed_hangul(self, char):
        # 한글 음절 여부 확인
        return '가' <= char <= '힣'

    def check_word(self, word):
        word = self.compose(word)
        if word is None:
            return False
        for char in word:
            if not self.is_correctly_composed_hangul(char):
                return False
        return True
