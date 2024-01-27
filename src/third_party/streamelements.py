import requests


class StreamElementsTTS:
    def __init__(self, voice):
        self.voice = voice

    def get_url(self, text):
        if text is None:
            return None

        try:
            url = f"https://api.streamelements.com/kappa/v2/speech?voice={self.voice.name}&text={text}"

            print("Speaking: ", text)

            res = requests.get(url)
            return res.url

        except Exception as e:
            print("Error getting StreamElements TTS URL: ", e)
            print("Response: ", res.text)
            return None
