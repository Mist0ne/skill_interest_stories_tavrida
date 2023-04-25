import json
from pathlib import Path

import pytest

from skill_interest_stories_tavrida.skill import skill

base_req_file_name = Path(__file__).parent / 'base_request.json'


# flake8: noqa
@pytest.mark.parametrize('phrase_text, new_session, answer_text', [
    ('тест', False, "Извините, не поняла. Скажите «начать» чтобы послушать вдохновляющую историю"),
])
def test_skill(phrase_text, new_session, answer_text):
    req = {}
    resp = {}
    with open(base_req_file_name) as f:
        req = json.load(f)

    req['request']['original_utterance'] = phrase_text
    req['request']['command'] = phrase_text
    req['session']['new'] = new_session

    skill.handle_dialog(req, resp)

    assert answer_text in resp['response']['text']
