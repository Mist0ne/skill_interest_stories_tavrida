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
        res['session_state'] = {'order': generate_order()}

    elif original_utterance in main_phrases.next_synonyms or original_utterance in main_phrases.more_synonyms:
        if len(req['state']['session']['order']) == 0:
            new_order = generate_order()
            random_phrase = main_phrases.stories[new_order[0]]
            res['session_state'] = {'order': new_order[1:]}
        else:
            random_phrase = main_phrases.stories[req['state']['session']['order'][0]]
            res['session_state'] = {'order': req['state']['session']['order'][1:]}

        res['response']['text'] = random_phrase['text']
        res['response']['tts'] = random_phrase['tts']
        res['response']['buttons'] = main_phrases.next_suggests
        res['response']['audio_player'] = {
            'playlist': [
                {
                    'stream': {
                        'track_id': random_phrase['audio_url'],
                        'source_type': 'url',
                        'source': random_phrase['audio_url']
                    },
                    'meta': {
                        'title': random_phrase['audio_title'],
                        'sub_title': random_phrase['audio_subtitle']
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
        res['session_state']['order'] = req['state']['session']['order']
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


def generate_order() -> list:
    order = list(range(len(main_phrases.stories)))
    random.shuffle(order)
    return order
