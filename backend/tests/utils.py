


from src.models.question import QuestionType

def create_module(*, title: str, items: list):
    return {
        "title": title,
        "items": items
    }

def create_module_item(*, article_id: int, title: str):
    return {
        "title": title,
        "article_id": article_id,
    }

def create_article(*, content: str, test_pk: int | None = None):
    return {
        "content": content,
        "test_pk": test_pk
    }


def create_test(*, title: str, questions: list):
    return {
        "title": title,
        "questions": questions
    }

def create_question(*, text: str, type: QuestionType, answers: list):
    return {
        "text": text,
        "type": type.value,
        "answers": answers
    }

def create_answer(*, text: str, is_correct: bool):
    return {
        "text": text,
        "is_correct": is_correct
    }



