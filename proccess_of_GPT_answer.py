
def extract_segment_descriptions(text):
    """
    Преобразует текст с описаниями сегментов в список чистых описаний,
    удаляя лишние префиксы и делая первую букву заглавной.
    
    :param text: str — исходный текст
    :return: list[str] — список отформатированных описаний
    """
    lines = text.strip().splitlines()
    descriptions = []

    for line in lines:
        parts = line.split(";", 1)
        if len(parts) == 2:
            desc = parts[1].strip()
            prefix = "Краткое описание представителя сегмента:"
            if desc.lower().startswith(prefix.lower()):
                desc = desc[len(prefix):].strip()
            # Первая буква — заглавная
            if desc:
                desc = desc[0].upper() + desc[1:]
            descriptions.append(desc)

    return descriptions




