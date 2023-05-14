import os
import tempfile

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

tmpdir = tempfile.mkdtemp()
tmpfile = os.path.join(tmpdir, 'out.mp3')


def speechja(stext: str):
    tts = gTTS(stext, lang="ja")
    tts.save(tmpfile)

    sound = AudioSegment.from_mp3(tmpfile)
    play(sound)


def main():
    msg = "はい、お元気ですか？"
    speechja(msg)

    beep = AudioSegment.from_mp3("/home/pi/button.mp3")
    play(beep)


if __name__ == "__main__":
    main()
