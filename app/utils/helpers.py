import re
import unicodedata


def slugify(text: str) -> str:
    if not text:
        return ""

    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower()

    text = re.sub(r"[^a-z0-9]+", "-", text)

    text = text.strip("-")

    return text


# def generate_subject_code(name: str) -> str:
#     if not name:
#         return ""
#
#     words = name.split()
#     code = "_".join(word.upper() for word in words if word)
#
#     return code


# def build_relations(include: list[str] | None):
#     options = []
#
#     if not include:
#         return options
#
#     if "questions" in include:
#         options.append(selectinload(Quiz.questions))
#
#     if "subject" in include:
#         options.append(selectinload(Quiz.subject))
#
#     return options