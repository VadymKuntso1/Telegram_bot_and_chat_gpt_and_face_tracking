import openai
from gtts import gTTS
import os

openai.api_key = "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"
while True:

    message = input('Напишыть питання')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": "Ти - чатбот, який відповідає реченням до 15 слів"},
                {"role": "user", "content": message},
            ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    tts = gTTS(text=result, lang='uk')
    tts.save("good.mp3")
    os.system("good.mp3")
    print()

