from main import TextHolder


def test_text_list_is_empty_by_defaut():
    assert TextHolder().texts == []
