from typing import Dict


def calculate_jakkards_coefficent(a: int, b: int, c: int) -> float:
    return c / (a + b - c)


def get_string_char_counts(string: str) -> Dict[chr, int]:
    result = {}
    for c in string:
        if c in result:
            result[c] = result[c] + 1
        else:
            result[c] = 1
    return result


def get_char_counts_intersection(a: Dict[chr, int], b: Dict[chr, int]) -> Dict[chr, int]:
    result = {}
    for c in a:
        if c in b:
            if not(c in result):
                if a[c] > b[c]:
                    result[c] = b[c]
                else:
                    result[c] = a[c]
    return result


def get_char_count(char_counts: Dict[chr, int]) -> int:
    count = 0
    for c in char_counts:
        count += char_counts[c]
    return count


def calculate_strings_jakkards_coefficent(stringA: str, stringB: str) -> float:
    a_char_counts = get_string_char_counts(stringA)
    b_char_counts = get_string_char_counts(stringB)
    char_counts_intersection = get_char_counts_intersection(a_char_counts, b_char_counts)

    a = get_char_count(a_char_counts)
    b = get_char_count(b_char_counts)
    c = get_char_count(char_counts_intersection)

    return calculate_jakkards_coefficent(a, b, c)
