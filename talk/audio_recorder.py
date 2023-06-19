import audioop
import wave

import pyaudio

# カード番号
# RPi で `arecord -l` 実行し検知したUSB マイクのハードウェアのカード番号を設定する
CARD_NUM = 0


class AudioRecorder:
    def __init__(self, chunk=4096, channel=1, rate=44100, threshold=1200):
        self.chunk = chunk
        self.format = pyaudio.paInt16
        self.channel = channel
        self.rate = rate
        self.threshold = threshold
        self.silent_chunk = 3 * rate / chunk  # 3 seconds
        self.frames = []
        self.audio = pyaudio.PyAudio()

    def start_record(self):
        stream = self.audio.open(
            format=self.format,
            channels=self.channel,
            rate=self.rate,
            input_device_index=CARD_NUM,
            input=True,
            output=False,
            frames_per_buffer=self.chunk,
        )

        silent_chunks = 0
        while True:
            data = stream.read(self.chunk)
            rms = audioop.rms(data, 2)
            if rms < self.threshold:
                silent_chunks += 1
                if silent_chunks > self.silent_chunk:
                    break
            else:
                silent_chunks = 0
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

    def save_recording(self, file_path):
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.channel)
        wf.setsampwidth(self.audio.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(self.frames))
        wf.close()


if __name__ == '__main__':
    recorder = AudioRecorder()
    recorder.start_record()
    recorder.save_recording('record.wav')
