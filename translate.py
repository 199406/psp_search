from deep_translator import GoogleTranslator


def eng_to_gel(text):
    return GoogleTranslator(source='en', target='ka').translate(text)


def gel_to_eng(text):
    return GoogleTranslator(source='ka', target='en').translate(text)