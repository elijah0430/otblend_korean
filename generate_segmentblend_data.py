# generate_segmentblend_data.py

import csv
from tqdm.auto import tqdm
from segmentblend import Segmentblend
from hangul_processor import HangulProcessor

class SegmentblendDataGenerator:
    def __init__(self):
        self.exceptions = set()
        self.processor = HangulProcessor()

    def get_random_noun(self):
        # Implement this method to fetch random Korean nouns.
        # For demonstration purposes, we'll use a predefined list.
        nouns = ["사과", "바나나", "자동차", "컴퓨터", "학교", "책상", "의자", "강아지", "고양이", "집"]
        import random
        random_noun = random.choice(nouns)
        while random_noun in self.exceptions or len(random_noun) <= 1:
            random_noun = random.choice(nouns)
        self.exceptions.add(random_noun)
        return random_noun

    def generate_segmentblend_data(self, num_entries=2):
        with open('segmentblend_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Word1", "Word2", "Head", "Order_Candidates"])

            for _ in tqdm(range(num_entries)):
                word1 = None
                word2 = None

                while word1 is None:
                    random_noun = self.get_random_noun()
                    if len(random_noun) > 1:
                        word1 = random_noun

                while word2 is None:
                    random_noun = self.get_random_noun()
                    if len(random_noun) > 1:
                        word2 = random_noun

                segmentblend = Segmentblend(word1, word2, head=1)
                top_candidates = segmentblend.order_candidates()

                # Convert candidate data to a string for CSV writing
                candidates_str = '; '.join([f"{candidate}:{score}" for candidate, score in top_candidates])

                writer.writerow([word1, word2, 1, candidates_str])

if __name__ == "__main__":
    generator = SegmentblendDataGenerator()
    generator.generate_segmentblend_data(num_entries=1000)
