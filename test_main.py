from main import PhrasesHolder
import pytest


def test_initially_there_are_no_phrases():
    assert PhrasesHolder().phrases == set()


def test_can_add_new_phrase():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    assert phrase_holder.phrases == {'hello'}


def test_cannot_add_the_same_phrase_twice():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(ValueError):
        phrase_holder.add_phrase('hello')


def test_adding_new_phrases_ignores_letter_case():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(ValueError):
        phrase_holder.add_phrase('HeLlO')


def test_first_letter_of_a_new_phrase_must_be_unique():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(ValueError):
        phrase_holder.add_phrase('hi')
