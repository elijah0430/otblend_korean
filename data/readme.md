# Quick Start Guide

This guide provides concise instructions for using the `random_noun.py`, `sample_data.py`, and `generate_data.py` scripts. These scripts are designed to retrieve random Korean nouns, process words using the `OTblend` or `Segmentblend` methods, and generate OTblend data, respectively.

## Using `random_noun.py`

The `random_noun.py` script fetches a random Korean noun from the Standard Korean Dictionary (표준국어대사전) based on a given search word or randomly if no word is provided. It limits the results to single-word nouns.

### Command-Line Arguments

- `--word` (str): *(Optional)* The search word to query.
- `--pos` (int): *(Optional)* Part of speech. Default is `1` (noun).
- `--num` (int): *(Optional)* Number of results to retrieve. Default is `20`.
- `--letter_s` (int): *(Optional)* Length of the word. Default is `2`.

### Basic Usage

```bash
python random_noun.py [--word WORD] [--pos POS] [--num NUM] [--letter_s LENGTH]
```

### Examples

- Fetch a random noun:

  ```bash
  python random_noun.py
  ```

- Fetch a random noun related to "사랑" (love):

  ```bash
  python random_noun.py --word 사랑
  ```

- Fetch a noun of length 3:

  ```bash
  python random_noun.py --letter_s 3
  ```

### Notes

- **API Key Replacement**: Replace the placeholder `API_KEY` in the script with your actual API key. The placeholder (`512D7366AB4AD6ADCF673E923623DF35`) is not valid.

- **Part of Speech (`pos`) Values**:

  - `1`: Noun (Default)
  - Other values correspond to different parts of speech as defined by the API documentation.

- **Error Handling**: If no word is found after several attempts, the script will output:

  ```
  단어를 찾을 수 없습니다.
  ```

---

## Using `sample_data.py`

The `sample_data.py` script processes two words using either the `OTblend` or `Segmentblend` method.

### Command-Line Arguments

- `word1` (str): First word to process.
- `word2` (str): Second word to process.
- `--method` (str): *(Optional)* Method to use (`OTblend` or `Segmentblend`). Default is `OTblend`.
- `--head` (int): *(Optional)* Specify the head word (`1` or `2`). Default is `1`.

### Basic Usage

```bash
python sample_data.py word1 word2 [--method METHOD] [--head HEAD]
```

### Examples

- Using `OTblend` with default head:

  ```bash
  python sample_data.py 사랑 희망 --method OTblend
  ```

- Using `Segmentblend`:

  ```bash
  python sample_data.py 사랑 희망 --method Segmentblend
  ```

---

## Using `generate_data.py`

The `generate_data.py` script generates OTblend data by pairing random Korean nouns.

### Command-Line Arguments

- `--num_entries` (int): *(Optional)* Number of data entries to generate. Default is `1000`.

### Basic Usage

```bash
python generate_data.py [--num_entries NUM]
```

### Example

Generate 500 entries:

```bash
python generate_data.py --num_entries 500
```

---

**Note**: Ensure all scripts have the necessary permissions and dependencies installed before execution.