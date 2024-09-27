# segmentblend.py

from hangul_processor import HangulProcessor

class Segmentblend:
    def __init__(self, word1, word2, head=0):
        self.processor = HangulProcessor()
        self.word1 = word1
        self.word2 = word2
        self.head = head
        self.candidate_dic, self.candidate_ls = self.generate_candidates(head=self.head)
        self.candidate_score_dic = self.generate_candidate_score_dic()

    def __str__(self):
        return f"Segmentblend with words: '{self.word1}' and '{self.word2}'"

    def generate_candidates(self, head):
        if head == 0:
            word1 = self.word2
            word2 = self.word1
        else:
            word1 = self.word1
            word2 = self.word2

        # Generate prefixes of word1 and suffixes of word2
        word1_prefixes = [word1[:i] for i in range(1, len(word1)+1)]
        word2_suffixes = [word2[i:] for i in range(len(word2))]

        candidate_dict = {}
        for prefix in word1_prefixes:
            for suffix in word2_suffixes:
                candidate = prefix + suffix
                candidate_dict[candidate] = len(prefix) - 1

        candidate_ls = list(candidate_dict.keys())
        candidate_ls = [word for word in candidate_ls if self.processor.check_word(word)]
        candidate_ls = [word for word in candidate_ls if len(word) > 1]
        # Remove original words from candidates
        if word1 + word2 in candidate_ls:
            candidate_ls.remove(word1 + word2)
        if word1 in candidate_ls:
            candidate_ls.remove(word1)
        if word2 in candidate_ls:
            candidate_ls.remove(word2)
        candidate_ls = list(set(candidate_ls))

        return candidate_dict, candidate_ls

    def generate_candidate_score_dic(self):
        return {candidate: [0, 0, 0, 0, 0, 0] for candidate in self.candidate_ls}

    def blend(self):
        self.candidate_dic = self.apply_disc(self.candidate_score_dic, 0)
        self.candidate_dic = self.apply_max_dep(self.candidate_score_dic, 1, head=self.head)
        self.candidate_dic = self.apply_max_seg(self.candidate_score_dic, 2)
        self.candidate_dic = self.apply_morph_dis(self.candidate_score_dic, 3)
        self.candidate_dic = self.apply_oo_contiguity(self.candidate_score_dic, 4)
        self.candidate_dic = self.apply_segmental_conservation(self.candidate_score_dic, 5)

    # Constraint methods adjusted to work with original words
    def apply_disc(self, candidate_score_dic, index):
        if len(self.word1) >= len(self.word2):
            longer_word = self.word1
            shorter_word = self.word2
        else:
            longer_word = self.word2
            shorter_word = self.word1
        sublen = len(longer_word) - len(shorter_word)

        for candidate in list(candidate_score_dic.keys()):
            switch = True
            for i, c in enumerate(candidate):
                if i < len(longer_word):
                    if c == longer_word[i] and (
                        (i < len(shorter_word) and c == shorter_word[i]) or
                        (i >= sublen and (i - sublen) < len(shorter_word) and c == shorter_word[i - sublen])
                    ):
                        switch = False
                        break
            if switch:
                candidate_score_dic[candidate][index] += 1

        return candidate_score_dic

    def apply_max_dep(self, candidate_score_dic, index, head):
        if head < 2:
            if head:
                longer_word = self.word2
                shorter_word = self.word1
            else:
                longer_word = self.word1
                shorter_word = self.word2
        elif len(self.word1) >= len(self.word2):
            longer_word = self.word1
            shorter_word = self.word2
        else:
            longer_word = self.word2
            shorter_word = self.word1
        for candidate in list(candidate_score_dic.keys()):
            dep = len(candidate) - len(longer_word)
            max1 = len(longer_word) - len(candidate)
            if dep > 0:
                candidate_score_dic[candidate][index] += dep
            if max1 > 0:
                candidate_score_dic[candidate][index] += max1
        return candidate_score_dic

    def apply_max_seg(self, candidate_score_dic, index):
        for candidate in list(candidate_score_dic.keys()):
            for i, char in enumerate(self.word1):
                if i < len(candidate):
                    if char != candidate[i]:
                        candidate_score_dic[candidate][index] += len(self.word1) - i
                        break
            for j, char in enumerate(self.word2):
                if self.word2[j:] == candidate[i:]:
                    break
                candidate_score_dic[candidate][index] += 1
        return candidate_score_dic

    def apply_morph_dis(self, candidate_score_dic, index):
        if len(self.word1) >= len(self.word2):
            longer_word = self.word1
            shorter_word = self.word2
        else:
            longer_word = self.word2
            shorter_word = self.word1
        sublen = len(longer_word) - len(shorter_word)

        for candidate in list(candidate_score_dic.keys()):
            for i, c in enumerate(candidate):
                if i < len(longer_word):
                    if c == longer_word[i] and (
                        (i < len(shorter_word) and c == shorter_word[i]) or
                        (i >= sublen and (i - sublen) < len(shorter_word) and c == shorter_word[i - sublen])
                    ):
                        candidate_score_dic[candidate][index] += 1
        return candidate_score_dic

    def apply_oo_contiguity(self, candidate_score_dic, index):
        if len(self.word1) >= len(self.word2):
            longer_word = self.word1
            shorter_word = self.word2
        else:
            longer_word = self.word2
            shorter_word = self.word1
        sublen = len(longer_word) - len(shorter_word)

        for candidate in list(candidate_score_dic.keys()):
            ls = []
            for i, c in enumerate(candidate):
                if i < len(longer_word):
                    if c == longer_word[i] and (
                        (i < len(shorter_word) and c == shorter_word[i]) or
                        (i >= sublen and (i - sublen) < len(shorter_word) and c == shorter_word[i - sublen])
                    ):
                        ls.append(i)
            if len(ls) > 1:
                for i in range(len(ls) - 1):
                    if ls[i + 1] - ls[i] > 1:
                        candidate_score_dic[candidate][index] += 1
        return candidate_score_dic

    def apply_segmental_conservation(self, candidate_score_dic, index):
        for candidate in list(candidate_score_dic.keys()):
            for seg in candidate:
                if seg not in self.word1 and seg not in self.word2:
                    candidate_score_dic[candidate][index] += 1
        return candidate_score_dic

    def order_candidates(self, length=5):
        self.blend()
        sorted_candidates = sorted(self.candidate_score_dic.items(), key=lambda item: item[1])
        top_candidates = sorted_candidates[:length]
        return top_candidates

    def score_candidate(self, candidate):
        sorted_candidates = sorted(self.candidate_score_dic.items(), key=lambda item: item[1])
        sorted_candidate_names = [item[0] for item in sorted_candidates]

        if candidate in sorted_candidate_names:
            return sorted_candidate_names.index(candidate) + 1
        else:
            return None  # Candidate not found
