# flake8: noqa: E501
import random
from . import main_phrases


def handle_dialog(req):
    res = dict()
    res['version'] = req['version']
    res['session'] = req['session']
    res['response'] = {
        'end_session': False
    }

    user_id = req['session']['user_id']
    original_utterance = req['request']['original_utterance'].lower()

    # Обрабатываем вход в скилл
    if req['session']['new']:
        random_welcome_text = random.choice(main_phrases.welcome_texts)
        res['response']['text'] = random_welcome_text['text']
        res['response']['tts'] = random_welcome_text['tts']
        res['response']['buttons'] = main_phrases.welcome_suggest

    elif original_utterance in main_phrases.next_synonyms or original_utterance in main_phrases.more_synonyms:
        random_phrase = random.choice(main_phrases.next_phrases)
        res['response']['text'] = random_phrase['text']
        res['response']['tts'] = random_phrase['tts']
        res['response']['buttons'] = main_phrases.next_suggests
        res['response']['audio_player'] = {
            'playlist': [
                {
                    'stream': {
                        'track_id': '2000512019_456239032',
                        'source_type': 'vk',
                        'source': '2000512019_456239032'
                    },
                    'meta': {
                        'title': 'title',
                        'sub_title': 'subtitle'
                    }
                }
            ]
        }

    elif original_utterance in main_phrases.stop_synonyms:
        random_phrase = random.choice(main_phrases.exit_phrases)
        res['response']['text'] = random_phrase['text']
        res['response']['tts'] = random_phrase['tts']
        res['response']['end_session'] = True

    else:
        res['response']['text'] = main_phrases.unclear['text']
        res['response']['tts'] = main_phrases.unclear['tts']
        res['response']['buttons'] = main_phrases.welcome_suggest
        if 'errors_count' in req['state']['session']:
            if req['state']['session']['errors_count'] >= 2:
                random_phrase = random.choice(main_phrases.exit_phrases)
                res['response']['text'] = random_phrase['text']
                res['response']['tts'] = random_phrase['tts']
                res['response']['end_session'] = True
                res['response']['buttons'] = []
            else:
                res['session_state'] = {'errors_count': req['state']['session']['errors_count'] + 1}
        else:
            res['session_state'] = {'errors_count': 1}

    return res
