import re

def clear_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clear_integer(text_with_number: str) -> int:
    return int(re.sub(r"\D", "", text_with_number))
