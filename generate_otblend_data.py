import csv
from tqdm.auto import tqdm
from otblend import OTblend

class OTblendDataGenerator:
    def __init__(self):
        self.exceptions = set()
        self.processor = HangulProcessor()

    def get_random_noun(self):
        # 랜덤 명사를 가져오는 함수 구현 필요
        # 이 예시에서는 임의의 명사 리스트에서 선택하도록 합니다.
        nouns = ["사과", "바나나", "자동차", "컴퓨터", "학교", "책상", "의자", "강아지", "고양이", "집"]
        import random
        random_noun = random.choice(nouns)
        while random_noun in self.exceptions or len(random_noun) <= 1:
            random_noun = random.choice(nouns)
        self.exceptions.add(random_noun)
        return random_noun

    def generate_otblend_data(self, num_entries=2):
        with open('otblend_data.csv', mode='w', newline='', encoding='utf-8') as file:
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

                otblend = OTblend(word1, word2, head=1)
                order_candidates = otblend.order_candidates()

                writer.writerow([word1, word2, 1, order_candidates])

if __name__ == "__main__":
    generator = OTblendDataGenerator()
    generator.generate_otblend_data(num_entries=1000)
