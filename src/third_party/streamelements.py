from urllib.parse import quote


class StreamElementsTTS:
    def __init__(self, voice):
        self.voice = voice

    def get_url(self, text):
        if text is None:
            return None

        url = f"https://api.streamelements.com/kappa/v2/speech?voice={self.voice.name}&text={text}"
        return quote(url, safe=':/?&=')
