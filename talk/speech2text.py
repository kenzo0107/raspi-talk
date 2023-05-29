import io

# speech to text API を利用するので有料
# see: https://cloud.google.com/speech-to-text/pricing
from google.cloud import speech


class Speech2Text:
    def __init__(
        self,
        audio_filename,
        credentials_filepath='cloud-speech-to-text-api-key.json',
        rate=44100,
        language_code='en-US',
    ):
        self.audio_filename = audio_filename
        self.language_code = language_code
        self.rate = rate
        self.client = speech.SpeechClient.from_service_account_json(
            credentials_filepath
        )

    def recognize(self):
        # 音声ファイルの読み込み
        with io.open(self.audio_filename, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)

        # 音声を Google Cloud Speech-to-Text API に送信してテキストに変換
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.rate,
            language_code=self.language_code,
        )

        # 変換されたテキストを取得
        r = self.client.recognize(config=config, audio=audio)
        transcripts = [result.alternatives[0].transcript for result in r.results]
        return ' '.join(transcripts)


if __name__ == '__main__':
    s2t = Speech2Text('record.wav', language_code='ja-JP')
    text = s2t.recognize()
    print(text)
