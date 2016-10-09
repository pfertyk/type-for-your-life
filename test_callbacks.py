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


def test_rcc_not_called_when_phrase_matches_first_character(mocker):
    rcc = mocker.stub()
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.add_phrase('hello')
    phrase_holder.send_char('h')
    rcc.assert_not_called()


def test_rcc_called_when_subsequent_character_is_incorrect(mocker):
    rcc = mocker.stub()
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.add_phrase('hello')
    phrase_holder.send_char('h')
    phrase_holder.send_char('a')
    rcc.assert_called_once_with('a')


def test_rcc_not_called_when_subsequent_character_is_correct(mocker):
    rcc = mocker.stub()
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.add_phrase('hello')
    phrase_holder.send_char('h')
    rcc.assert_not_called()


def test_can_define_accepted_char_callback():
    PhrasesHolder(accepted_char_callback=lambda a, b, c: None)


def test_acc_called_when_first_character_matches(mocker):
    acc = mocker.stub()
    phrase_holder = PhrasesHolder(accepted_char_callback=acc)
    phrase_holder.add_phrase('hello')
    phrase_holder.send_char('h')
    acc.assert_called_with('h', 'hello', 'ello')
