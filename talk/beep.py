import numpy as np
from pydub import AudioSegment
from pydub.playback import play


class BeepSoundPlayer:
    def __init__(self, sample_rate=44100, freq=220, duration=0.2):
        self.sample_rate = sample_rate
        self.freq = freq
        self.duration = duration
        self.beep = self._generate_beep_sound()

    def _generate_beep_sound(self):
        t = np.arange(0, self.duration, 1 / self.sample_rate)
        sine_wave = np.sin(2 * np.pi * self.freq * t) * (2**15 - 1)
        sine_wave = sine_wave.astype(np.int16)

        beep = AudioSegment(
            sine_wave.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=sine_wave.dtype.itemsize,
            channels=1,
        )
        return beep

    def play_beep_sound(self):
        play(self.beep)


if __name__ == '__main__':
    player = BeepSoundPlayer()
    player.play_beep_sound()
