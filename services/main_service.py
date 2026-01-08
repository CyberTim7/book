import re



def _get_page(text, start, size):
    new_text = re.sub(r"[.,!?:;]\.+$", "", text[start:start + size])
    a = 0
    for c in new_text:
        if c in '.,!?:;':
            a += 1
            break
    if a == 0:
        new_text = new_text + ".."

    new_text = re.findall(r"(?s).+[.,!?:;]", new_text)
    return *new_text, len(*new_text)


def get_book(text, size=1050):
    start = 0
    page = 0
    book = {}
    if len(text) == 0:
        return False
    while start < len(text):
        page += 1
        result = _get_page(text, start, size)
        book[page] = result[0].strip()
        start += result[1]
    return book
