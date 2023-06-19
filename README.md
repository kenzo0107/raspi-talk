# raspi-talk

talk with raspberry pi

## System Overview

```mermaid
sequenceDiagram
    autonumber
    participant motion_sensor as MotionSensor
    actor user
    participant raspberrypi as RPi
    participant chat_gpt as ChatGPT
    participant googlecloud2speech as Google Cloud Speech-to-Text API
    motion_sensor->>user: motion detection
    motion_sensor->>raspberrypi: notify of motion detection
    raspberrypi->>chat_gpt: post `Hello`
    chat_gpt->>raspberrypi: response
    raspberrypi->>user: play `<response>` text
    loop
        user->>raspberrypi: speak to the mic
        raspberrypi->>raspberrypi: save audio spoken by the user
        Note Right of raspberrypi: = record.wav
        raspberrypi->>googlecloud2speech: post `audio`
        googlecloud2speech->>raspberrypi: speech to text
        raspberrypi->>chat_gpt: post `<text>`
        chat_gpt->>raspberrypi: response
        raspberrypi->>user: play `<response>` text on speaker
    end
    user-->>raspberrypi: do not talk for 5 seconds
    raspberrypi->>raspberrypi: end the conversation (return to No.1)
```

## Start Conversation

```console
$ python3 handler.py 2>/dev/null
```

`2>/dev/null` is added because the alsa related error log becomes noise.
I want to disable alsa error logs, but I don't know the way.

## License

[MIT License](https://github.com/kenzo0107/raspi-talk/blob/main/LICENSE)
