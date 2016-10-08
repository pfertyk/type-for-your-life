from main import TextHolder


def test_text_list_is_empty_by_defaut():
    assert TextHolder().texts == []


def test_can_add_text_to_list():
    text_holder = TextHolder()
    text_holder.add_text('hello')
    assert text_holder.texts == ['hello']
