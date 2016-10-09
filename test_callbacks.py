from main import PhrasesHolder


def test_can_define_rejected_char_callback():
    PhrasesHolder(rejected_char_callback=lambda a: None)


def test_rcc_called_when_no_phrase_is_available(mocker):
    rcc = mocker.stub()
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.send_char('a')
    rcc.assert_called_with('a')


def test_rcc_called_when_no_phrase_matches_first_character(mocker):
    rcc = mocker.stub()
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.add_phrase('hello')
    phrase_holder.send_char('a')
    rcc.assert_called_with('a')


def test_rcc_called_when_subsequent_character_is_incorrect(mocker):
    rcc = mocker.stub()
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.add_phrase('hello')
    phrase_holder.send_char('h')
    rcc.assert_not_called()
    phrase_holder.send_char('h')
    rcc.assert_called_with('h')


def test_can_define_accepted_char_callback():
    PhrasesHolder(accepted_char_callback=lambda a, b, c: None)
