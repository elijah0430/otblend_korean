# Quick Start Guide

This guide provides concise instructions for using the `sample_data.py` and `generate_data.py` scripts. These scripts are designed to process words using the `OTblend` or `Segmentblend` methods and to generate OTblend data, respectively.

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

- Using `Segmentblend` :

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
