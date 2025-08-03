def escape_markdown(text: str) -> str:
    """Экранирует символы markdown в тексте"""
    text = text.replace("-", "\\-")
    return text