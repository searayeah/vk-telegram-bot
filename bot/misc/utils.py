
def fix_text(self, text):
    if len(text) == 0:
        return "Ошибочка"  # а если фотография???))
    text = (
        text.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&amp;", "&")
    )
    for char in self.tg_prohibited_chars:
        text = text.replace(char, f"\\{char}")
    return text

def get_message_type(peer_id):
    if peer_id < 0:
        return "group"
    elif peer_id > int(2e9):
        return "chat"
    else:
        return "user"
