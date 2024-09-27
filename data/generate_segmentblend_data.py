import csv
from tqdm.auto import tqdm
import argparse
from random_noun import get_random_noun
from segmentblend import Segmentblend

def generate_segmentblend_data(exceptions, num_entries=2):
    with open('segmentblend_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Word1", "Word2", "Head", "Order_Candidates"])

        for _ in tqdm(range(num_entries), desc="Generating Segmentblend data"):
            word1 = None
            word2 = None

            for var in ["word1", "word2"]:
                while True:
                    random_noun, exceptions = get_random_noun(exceptions)
                    if random_noun is not None and len(random_noun) > 1:
                        if var == "word1":
                            word1 = random_noun
                        else:
                            word2 = random_noun
                        break

            segmentblend = Segmentblend(word1, word2, head=1)
            order_candidates = segmentblend.order_candidates()

            writer.writerow([word1, word2, 1, order_candidates])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Segmentblend 데이터를 생성합니다.')
    parser.add_argument('--num_entries', type=int, default=1000, help='생성할 데이터의 개수 (기본값: 1000)')
    args = parser.parse_args()

    exceptions = []
    generate_segmentblend_data(exceptions, args.num_entries)
