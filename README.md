# post-content-pilot

A Python tool that extracts insights from PDFs or web articles, summarizes content with AI, and generates posts automatically. Includes a confirmation step before publishing.

## Set Up Environments

### Python Environment

- Using Python versions 3.10.16

- Using Conda to manage

**Commands**

```bash
conda create -n post-content-pilot python=3.10

conda activate post-content-pilot
```

### Setup pre-commit

- Using pre-commit for making codes better.

**Commands**

```bash
pip install pre-commit

pre-commit run
```

### Requirements

- All in requirements.txt

**Commands**

```bash
pip install -r requirements.txt
```

## Usage

### Paper Summerize

```bash
python main.py --url_link <url> --file_path <file_path> --tone <tone> --target_platform <target_platform>
```

#### Parameters

- `url_link`: URL of the article or PDF to summarize.
- `file_path`: File path of the article or PDF to summarize.
- `tone`: Tone of the post (e.g., 'Professional', 'Casual').
- `target_platform`: Target platform for the post (e.g., 'LinkedIn', 'Twitter').

#### Output

The output will be a text file with the generated post.

### News Summerize

```bash
python main_v2.py --url_link <url> --tone <tone> --target_platform <target_platform>
```

#### Parameters

- `url_link`: URL of the article or PDF to summarize.
- `tone`: Tone of the post (e.g., 'Professional', 'Casual').
- `target_platform`: Target platform for the post (e.g., 'LinkedIn', 'Twitter').

#### Output

The output will be a text file with the generated post.

