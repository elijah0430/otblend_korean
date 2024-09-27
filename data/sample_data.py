import argparse
from otblend import OTblend
from segmentblend import Segmentblend

def main():
    parser = argparse.ArgumentParser(description='Process words with OTblend or Segmentblend.')
    parser.add_argument('word1', type=str, help='First word')
    parser.add_argument('word2', type=str, help='Second word')
    parser.add_argument('--head', type=int, default=1, choices=[1,2], help='Specify the head (1 or 2)')
    parser.add_argument('--method', type=str, default='OTblend', choices=['OTblend', 'Segmentblend'], help='Choose the method to use')
    args = parser.parse_args()

    word1 = args.word1
    word2 = args.word2
    head = args.head
    method = args.method

    if method == 'OTblend':
        processor = OTblend(word1, word2, head=head)
        result = processor.order_candidates()
    elif method == 'Segmentblend':
        processor = Segmentblend(word1, word2, head=head)
        result = processor.blend()
    else:
        print("Invalid method selected.")
        return

    print(f"Result using {method}: {result}")

if __name__ == '__main__':
    main()
