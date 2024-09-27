import requests
import random
import xml.etree.ElementTree as ET
import argparse

API_KEY = "512D7366AB4AD6ADCF673E923623DF35"  # 실제 API 키로 교체하세요
BASE_URL = "https://stdict.korean.go.kr/api/search.do"

def get_random_noun(exceptions, word=None, pos=1, num=10, letter_s=2):
    if word is None:
        word = chr(random.randint(0xAC00, 0xD7A3))
        while word in exceptions:
            word = chr(random.randint(0xAC00, 0xD7A3))
    params = {
        "key": API_KEY,
        "advanced": "y",
        "q": word,
        "pos": pos,
        "num": num,
        "sort": "dict",
        "method": "include",
        "type1": "word",
        "letter_s": letter_s
    }
    
    words = []
    retries = 0
    max_retries = 5

    while len(words) == 0 and retries < max_retries:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            words = [
                item.find('word').text
                for item in root.findall('.//item')
                if item.find('word') is not None and '-' not in item.find('word').text
            ]
            if words:
                return random.choice(words), exceptions
        else:
            exceptions.append(word)
            return None, exceptions
        retries += 1

    # 5번 시도 후에도 words가 비어있으면 처리
    if not words:
        return None, exceptions


def main():
    parser = argparse.ArgumentParser(description='랜덤 한국어 명사를 가져옵니다.')
    parser.add_argument('--word', type=str, help='검색할 단어')
    parser.add_argument('--pos', type=int, default=1, help='품사 (기본값: 1, 명사)')
    parser.add_argument('--num', type=int, default=20, help='가져올 결과 수 (기본값: 10)')
    parser.add_argument('--letter_s', type=int, default=2, help='단어의 길이 (기본값: 2)')
    args = parser.parse_args()

    exceptions = []
    random_noun, exceptions = get_random_noun(
        exceptions,
        word=args.word,
        pos=args.pos,
        num=args.num,
        letter_s=args.letter_s
    )

    if random_noun:
        print(f"랜덤 명사: {random_noun}")
    else:
        print("단어를 찾을 수 없습니다.")

if __name__ == '__main__':
    main()
