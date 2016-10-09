from main import PhrasesHolder


def test_can_define_rejected_char_callback():
    PhrasesHolder(rejected_char_callback=lambda x: None)


def test_rcc_called_when_no_phrase_is_available(mocker):
    rcc = mocker.stub(name='hello')
    phrase_holder = PhrasesHolder(rejected_char_callback=rcc)
    phrase_holder.send_char('a')
    rcc.assert_called_with('a')
