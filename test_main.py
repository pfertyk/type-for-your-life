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


def test_cannot_add_the_same_phrase_twice_ignoring_case():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(ValueError):
        phrase_holder.add_phrase('HeLlO')


def test_first_letter_of_a_new_phrase_must_be_unique():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(ValueError):
        phrase_holder.add_phrase('hi')


def test_first_letter_of_a_new_phrase_must_be_unique_ignoring_case():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('hello')
    with pytest.raises(ValueError):
        phrase_holder.add_phrase('Hi')


def test_initially_current_phrase_is_none():
    assert PhrasesHolder().current_phrase is None


def test_typing_first_character_of_phrase_makes_it_current_phrase():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('sup')
    phrase_holder.send_char('s')
    assert phrase_holder.current_phrase == 'sup'


def test_if_phrase_is_already_selected_than_new_phrase_cannot_be_selected():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('sup')
    phrase_holder.add_phrase('notmuch')
    phrase_holder.send_char('s')
    phrase_holder.send_char('n')
    assert phrase_holder.current_phrase == 'sup'


def test_selecting_current_phrase_ignores_case():
    phrase_holder = PhrasesHolder()
    phrase_holder.add_phrase('Sup')
    phrase_holder.send_char('s')
    assert phrase_holder.current_phrase == 'Sup'
