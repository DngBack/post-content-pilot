import tiktoken
from typing import List, Tuple, Optional

def tokenize(text: str, model_name: str = 'gpt-4o-mini'):
    """
    Tokenizes the input text using the tiktoken library.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    return encoding.encode(text)

def chunk_on_delimiter(input_string: str,
                       max_tokens: int,
                       delimiter: str,
                       model_name: str = 'gpt-4-turbo') -> List[str]:
    """
    Splits the input string on a delimiter and combines chunks to ensure they are within max_tokens.
    """
    chunks = input_string.split(delimiter)
    combined_chunks, _, dropped_chunk_count = combine_chunks_with_no_minimum(
        chunks, max_tokens, chunk_delimiter=delimiter, add_ellipsis_for_overflow=True, model_name=model_name
    )
    if dropped_chunk_count > 0:
        print(f"Warning: {dropped_chunk_count} chunks were dropped due to overflow.")
    combined_chunks = [f"{chunk}{delimiter}" for chunk in combined_chunks]
    return combined_chunks

def combine_chunks_with_no_minimum(
        chunks: List[str],
        max_tokens: int,
        chunk_delimiter="\n\n",
        header: Optional[str] = None,
        add_ellipsis_for_overflow=False,
        model_name: str = 'gpt-4-turbo',
) -> Tuple[List[str], List[int], int]:
    """
    Combines chunks without a minimum size, ensuring each is under max_tokens.
    """
    dropped_chunk_count = 0
    output = []
    output_indices = []
    candidate = [] if header is None else [header]
    candidate_indices = []
    for chunk_i, chunk in enumerate(chunks):
        chunk_with_header = [chunk] if header is None else [header, chunk]
        if len(tokenize(chunk_delimiter.join(chunk_with_header), model_name=model_name)) > max_tokens:
            print("Warning: Chunk overflow.")
            if (add_ellipsis_for_overflow and
                    len(tokenize(chunk_delimiter.join(candidate + ["..."]), model_name=model_name)) <= max_tokens):
                candidate.append("...")
                dropped_chunk_count += 1
            continue
        extended_candidate_token_count = len(tokenize(chunk_delimiter.join(candidate + [chunk]), model_name=model_name))
        if extended_candidate_token_count > max_tokens:
            output.append(chunk_delimiter.join(candidate))
            output_indices.append(candidate_indices)
            candidate = chunk_with_header
            candidate_indices = [chunk_i]
        else:
            candidate.append(chunk)
            candidate_indices.append(chunk_i)
    if (header is not None and len(candidate) > 1) or (header is None and len(candidate) > 0):
        output.append(chunk_delimiter.join(candidate))
        output_indices.append(candidate_indices)
    return output, output_indices, dropped_chunk_count
