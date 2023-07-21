import os
import time
import argparse
import yaml

import gpio
from audio_player import AudioPlayer
from audio_recorder import AudioRecorder
from beep import BeepSoundPlayer
from chat_bot_openai import ChatAPI
from dotenv import load_dotenv
from led import LED
from motion_sensor import MotionSensor
from speech2text import Speech2Text

if __name__ == '__main__':
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('-la', '--language', default='en')
    args = parser.parse_args()
    language_code = 'en-US'
    if args.language == 'ja':
        language_code = 'ja-JP'

    with open(f"locales.yml", "r") as file:
        d = yaml.safe_load(file)

    motionSensor = MotionSensor(gpio.MOTION_SENSOR)
    audioPlayer = AudioPlayer()
    beepSoundPlayer = BeepSoundPlayer()
    led = LED(led_pin=gpio.LED)

    system_context = {"role": "system", "content": d[args.language]['system_content']}

    conversation_context = [system_context]

    api_key = os.getenv('OPENAI_API_KEY')
    chat = ChatAPI(api_key, conversation_context)

    is_first = True
    is_detected = False
    is_no_reply = False
    user_utterance = ''
    response = ''

    while True:
        if not is_detected:
            is_detected = motionSensor.continuous_detect()
            print('detect you')
            continue
        if is_first:
            # 初回は自動で openai に挨拶から始める
            response = chat.post('Hello')
            is_first = False
        else:
            response = ''
            recorder = AudioRecorder()

            led.turn_on()
            beepSoundPlayer.play_beep_sound()
            recorder.start_record()
            recorder.save_recording('record.wav')
            led.turn_out()

            speech2text = Speech2Text('record.wav', language_code)

            try:
                # 音声ファイル record.wav から Cloud Speech-to-text API でテキストに変換
                user_utterance = speech2text.recognize()
                if user_utterance:
                    is_no_reply = False
                    print('=============== I say: `{}`'.format(user_utterance))
                    response = chat.post(user_utterance)
                else:
                    # 返事をしなかった場合、会話を終了させたい意図があると判定し5秒経過したら会話を終了する
                    # 念の為、もう一度だけ返事をするかチャンスは作り、それを無視した場合、会話を終了させる
                    if not is_no_reply:
                        is_no_reply = True
                        start_time = time.time()
                        time.sleep(5)
                        continue

                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 5:
                        # 意図的に exception を発生させ、初期化処理を実行する
                        raise BaseException

            except BaseException:
                # 会話を終了させる旨、chat bot に post する
                response = chat.post(d[args.language]['finish_post'])
                # 以下諸々初期化
                conversation_context.clear()
                conversation_context.append(system_context)
                is_first = True
                is_detected = False
                is_no_reply = False
                pass

        if response:
            print('=============== bot response: {}'.format(response))
            audioPlayer.text2speech(response, args.language)
        time.sleep(0.5)
