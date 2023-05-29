import os
import tempfile

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play


class AudioPlayer:
    def __init__(self):
        tmpdir = tempfile.mkdtemp()
        self.tmpfile = os.path.join(tmpdir, 'out.mp3')

    def text2speech(self, text: str, language='en'):
        tts = gTTS(text, lang=language)
        tts.save(self.tmpfile)
        self._play(self.tmpfile)

    def _play(self, path: str):
        sound = AudioSegment.from_file(path)
        play(sound)


if __name__ == '__main__':
    player = AudioPlayer()
    player.text2speech('Hello, World')
