# README

## Overview

This project provides a Python implementation for blending Korean words using Optimality Theory (OT). The code is structured in an object-oriented manner, encapsulating functionality into classes for modularity and reusability.

The main components of the project are:

- **`HangulProcessor`**: A class for handling Hangul (Korean script) processing tasks such as decomposition and composition of Hangul syllables.
- **`OTblend`**: A class that generates blended words from two input words based on OT constraints.
- **`OTblendDataGenerator`**: A class that generates blended word data and saves the results into a CSV file.

## File Structure

- `hangul_processor.py`: Contains the `HangulProcessor` class.
- `otblend.py`: Contains the `OTblend` class.
- `generate_otblend_data.py`: Contains the `OTblendDataGenerator` class.
- `otblend_data.csv`: The CSV file that will be generated containing blended word data.

## Dependencies

- Python 3.x
- Standard Python libraries: `unicodedata`, `csv`
- Third-party library: `tqdm` (for progress bars)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/otblend.git
   cd otblend
   ```

2. **Install Required Libraries**

   Install the `tqdm` library if you haven't already:

   ```bash
   pip install tqdm
   ```

## Usage

### 1. Hangul Processing

The `HangulProcessor` class handles the decomposition and composition of Hangul syllables.

**Example:**

```python
from hangul_processor import HangulProcessor

processor = HangulProcessor()

word = "안녕하세요"
decomposed = processor.decompose(word)
print(f"Decomposed: {decomposed}")

composed = processor.compose(decomposed)
print(f"Composed: {composed}")
```

### 2. Blending Words with OTblend

The `OTblend` class generates blended words from two input words based on Optimality Theory constraints.

**Example:**

```python
from otblend import OTblend

word1 = "사과"
word2 = "바나나"

otblend_instance = OTblend(word1, word2, head=1)
top_candidates = otblend_instance.order_candidates()

print("Top Blended Candidates:")
for candidate, score in top_candidates:
    print(f"Candidate: {candidate}, Score: {score}")
```

### 3. Generating Blended Word Data

Use the `OTblendDataGenerator` class to generate blended word data and save it to a CSV file.

**Example:**

```bash
python generate_otblend_data.py
```

This script will generate a file named `otblend_data.csv` containing the blended words and their associated scores.

### Customizing Data Generation

In the `generate_otblend_data.py` file, you can specify the number of entries you wish to generate:

```python
if __name__ == "__main__":
    generator = OTblendDataGenerator()
    generator.generate_otblend_data(num_entries=1000)
```

### Implementing the `get_random_noun` Method

The `get_random_noun` method in the `OTblendDataGenerator` class is a placeholder. You need to implement this method to fetch random Korean nouns from a data source such as a file, database, or API.

**Example Implementation:**

```python
def get_random_noun(self):
    import random
    # Load nouns from a text file
    with open('korean_nouns.txt', 'r', encoding='utf-8') as file:
        nouns = [line.strip() for line in file.readlines()]
    random_noun = random.choice(nouns)
    while random_noun in self.exceptions or len(random_noun) <= 1:
        random_noun = random.choice(nouns)
    self.exceptions.add(random_noun)
    return random_noun
```

**Note:** Ensure you have a `korean_nouns.txt` file containing a list of Korean nouns, one per line.

## Classes and Methods

### HangulProcessor

- **`decompose_hangul_char(char)`**
  - Decomposes a single Hangul character into its components.
- **`decompose(word)`**
  - Decomposes an entire word into Hangul components, excluding the silent consonant 'ᄋ'.
- **`insert_ieung_if_two_vowels_in_a_row(word)`**
  - Inserts the silent consonant 'ᄋ' when two vowels appear consecutively.
- **`recompose_diphthongs(word)`**
  - Recombines decomposed diphthongs into their original form.
- **`compose(word)`**
  - Composes decomposed Hangul components back into a word.
- **`is_correctly_composed_hangul(char)`**
  - Checks if a character is a correctly composed Hangul syllable.
- **`check_word(word)`**
  - Validates if a word is correctly composed in Hangul.

### OTblend

- **`__init__(word1, word2, head=0)`**
  - Initializes the OTblend instance with two words and a head parameter.
- **`generate_candidates(head)`**
  - Generates candidate blended words based on the head parameter.
- **`generate_candidate_score_dic()`**
  - Initializes a dictionary to store candidate scores.
- **`blend()`**
  - Applies OT constraints to score each candidate.
- **`apply_disc(candidate_score_dic, index)`**
  - Applies the 'Discontinuity' constraint.
- **`apply_max_dep(candidate_score_dic, index, head)`**
  - Applies the 'MAX/DEP' constraint.
- **`apply_max_seg(candidate_score_dic, index)`**
  - Applies the 'MAX-segmental' constraint.
- **`apply_morph_dis(candidate_score_dic, index)`**
  - Applies the 'Morphological Disparity' constraint.
- **`apply_oo_contiguity(candidate_score_dic, index)`**
  - Applies the 'Output-Output Contiguity' constraint.
- **`apply_segmental_conservation(candidate_score_dic, index)`**
  - Applies the 'Segmental Conservation' constraint.
- **`order_candidates(length=5)`**
  - Returns the top candidates based on their scores.
- **`score_candidate(candidate)`**
  - Returns the rank of a specific candidate.

### OTblendDataGenerator

- **`__init__()`**
  - Initializes the data generator with an empty set of exceptions and a `HangulProcessor` instance.
- **`get_random_noun()`**
  - Retrieves a random Korean noun (needs implementation).
- **`generate_otblend_data(num_entries=2)`**
  - Generates blended word data and saves it to `otblend_data.csv`.

## Example Workflow

1. **Process Hangul Words**

   ```python
   from hangul_processor import HangulProcessor

   processor = HangulProcessor()
   word = "학교"
   decomposed = processor.decompose(word)
   composed = processor.compose(decomposed)
   print(f"Decomposed: {decomposed}")
   print(f"Composed: {composed}")
   ```

2. **Blend Two Words**

   ```python
   from otblend import OTblend

   word1 = "강아지"
   word2 = "고양이"
   otblend_instance = OTblend(word1, word2, head=1)
   top_candidates = otblend_instance.order_candidates()

   print("Top Blended Candidates:")
   for candidate, score in top_candidates:
       print(f"Candidate: {candidate}, Score: {score}")
   ```

3. **Generate Blended Word Data**

   ```bash
   python generate_otblend_data.py
   ```

## Notes

- Ensure that the `get_random_noun` method is properly implemented to fetch nouns from your data source.
- The default nouns provided in the examples are placeholders and should be replaced with actual data for meaningful results.
- The `head` parameter in the `OTblend` class determines which word is considered the 'head' in blending. Adjust this parameter as needed.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have suggestions or encounter any problems.

