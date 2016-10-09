from main import PhrasesHolder
import pytest


def test_phrase_list_is_empty_by_defaut():
    assert PhrasesHolder().phrases == []


def test_can_add_phrase_to_list():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    assert phrase_holder.phrases == ['hello']


def test_cannot_add_the_same_phrase_twice():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(Exception):
        phrase_holder.add_phrase('hello')


def test_adding_new_phrase_ignores_letter_case():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(Exception):
        phrase_holder.add_phrase('HeLlO')
