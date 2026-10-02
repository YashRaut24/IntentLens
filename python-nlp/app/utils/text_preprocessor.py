import re
import unicodedata

CONTRACTIONS = {
    "what's": "what is",
    "how's": "how is",
    "where's": "where is",
    "i'm": "i am",
    "i've": "i have",
    "i'll": "i will",
    "i'd": "i would",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't": "cannot",
    "couldn't": "could not",
    "won't": "will not",
    "shouldn't": "should not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "hasn't": "has not",
    "haven't": "have not",
    "it's": "it is",
    "let's": "let us",
}

def clean_text(text: str) -> str:
    """
    Cleans and normalizes student query text:
    - Normalizes unicode characters
    - Expands common English contractions
    - Strips noisy punctuation while keeping domain tokens (like C++, C#, .js)
    - Normalizes multi-spaces
    """
    if not text or not isinstance(text, str):
        return ""

    # Normalize unicode
    text = unicodedata.normalize("NFKD", text)

    # Lowercase for uniform processing
    text = text.lower()

    # Contraction expansion
    for contraction, expansion in CONTRACTIONS.items():
        text = re.sub(r"\b" + re.escape(contraction) + r"\b", expansion, text)

    # Preserve special tech symbols temporarily if needed
    text = text.replace("c++", "cplusplus")
    text = text.replace("c#", "csharp")
    text = text.replace(".js", "js")
    text = text.replace(".net", "dotnet")

    # Remove non-alphanumeric except space and hyphen
    text = re.sub(r"[^\w\s\-]", " ", text)

    # Restore tech markers
    text = text.replace("cplusplus", "c++")
    text = text.replace("csharp", "c#")

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text
