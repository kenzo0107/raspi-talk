import os
import sys
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


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        msg = args[1]
    else:
        msg = "はい、お元気ですか？"
    print(msg)
    speechja(msg)

    beep = AudioSegment.from_mp3("/home/pi/button.mp3")
    play(beep)
