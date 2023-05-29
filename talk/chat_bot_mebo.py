import json
import os

import requests
from dotenv import load_dotenv


class MeboAPI:
    def __init__(self, api_key, agent_id, uid):
        self.api_key = api_key
        self.agent_id = agent_id
        self.uid = uid

    def post(self, utterance: str):
        self.utterance = utterance
        return self._completion()

    def _completion(self):
        d = {
            "api_key": self.api_key,
            "agent_id": self.agent_id,
            "uid": self.uid,
            "utterance": self.utterance,
        }
        response = requests.post(
            url='https://api-mebo.dev/api',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(d),
        )

        data = None
        if response.status_code == requests.codes.ok:
            text = response.text
            data = json.loads(text)
        return data


if __name__ == '__main__':
    load_dotenv()
    api_key = os.getenv('MEBO_API_KEY')
    agent_id = os.getenv('MEBO_AGENT_ID')
    uid = os.getenv('MEBO_UID')

    c = MeboAPI(api_key, agent_id, uid)
    r = c.post("おはようございます！")
    print(r)
