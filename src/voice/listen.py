import asyncio
import re
from datetime import datetime, timedelta

import numpy as np
import speech_recognition as sr
import torch
import whisper

# Heavily based on davabase/whisper_real_time for real time transcription
# https://github.com/davabase/whisper_real_time/tree/master

WAKE_WORDS = ["ok billy", "yo billy", "okay billy", "hey billy"]


class Listen():
    def __init__(self) -> None:
        self.should_stop = False
        self.data_queue = asyncio.Queue()

    def stop(self):
        self.should_stop = True

    async def process_audio_queue(self, phrase_timeout: float):
        now = datetime.utcnow()
        transcription = ['']
        # The last time a recording was retrieved from the queue.
        phrase_time = None
        while not self.should_stop:
            phrase_complete = False
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                phrase_complete = True
            # This is the last time we received new audio data from the queue.
            phrase_time = now

            audio_data = await self.data_queue.get()  # Get data asynchronously

            # Convert in-ram buffer to something the model can use directly without needing a temp file.
            # Convert data from 16 bit wide integers to floating point with a width of 32 bits.
            # Clamp the audio stream frequency to a PCM wavelength compatible default of 32768hz max.
            audio_np = np.frombuffer(
                audio_data, dtype=np.int16).astype(np.float32) / 32768.0

            # Read the transcription.
            result = await asyncio.to_thread(
                self.audio_model.transcribe,
                audio_np,
                fp16=torch.cuda.is_available()
            )

            text = result['text'].strip()
            if phrase_complete:
                transcription.append(text)
            else:
                transcription[-1] = text

            # Process transcript in the background.
            await self.process_transcript(transcription[-1])

            await asyncio.sleep(0.25)  # Non-blocking sleep

    async def start(self, action_queue: asyncio.Queue):
        self.action_queue = action_queue
        self.audio_queue = asyncio.Queue()
        non_english = False

        # We use SpeechRecognizer to record our audio because it has a nice feature where it can detect when speech ends.
        recorder = sr.Recognizer()
        recorder.energy_threshold = 1000
        # Definitely do this, dynamic energy compensation lowers the energy threshold dramatically to a point where the SpeechRecognizer never stops recording.
        recorder.dynamic_energy_threshold = False

        # print device index and name
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"{index}. \"{name}\"")

        device_index = int(input("Enter Microphone device index: "))
        source = sr.Microphone(device_index, sample_rate=16000)

        # Load / Download model
        model = "medium"
        if model != "large" and not non_english:
            model = model + ".en"
        self.audio_model = whisper.load_model(model)

        # These could be fine-tuned. I'm not sure what the best values are.
        record_timeout = 6
        phrase_timeout = 3

        with source:
            recorder.adjust_for_ambient_noise(source)

        loop = asyncio.get_running_loop()

        def record_callback(_, audio: sr.AudioData) -> None:
            """
            Threaded callback function to receive audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            # This function will be called from a background thread
            data = audio.get_raw_data()

            # Schedule the data to be put into the queue in the thread-safe manner
            loop.call_soon_threadsafe(self.data_queue.put_nowait, data)

        # Create a background thread that will pass us raw audio bytes.
        # We could do this manually but SpeechRecognizer provides a nice helper.
        recorder.listen_in_background(
            source, record_callback, phrase_time_limit=record_timeout
        )

        # Cue the user that we're ready to go.
        print("Billy is listening...\n")

        await self.process_audio_queue(phrase_timeout)

    def find_wake_word_start(self, line):
        normalized_line = line.lower()
        normalized_line = re.sub(r'[^a-zA-Z ]', '', normalized_line)

        wake_word_positions = [normalized_line.find(
            wake_word) for wake_word in WAKE_WORDS if wake_word in normalized_line]
        if not wake_word_positions:
            return -1

        return min(pos for pos in wake_word_positions if pos >= 0)

    async def process_transcript(self, line):
        wake_word_start = self.find_wake_word_start(line)
        if wake_word_start == -1:
            return  # No wake word found

        # Slice the line from the first wake word
        # it isn't perfect, but it's good enough
        processed_line = line[wake_word_start:]

        print("*" * 80)
        print("* ", processed_line)
        print("*" * 80)

        await self.run_tool_tree(processed_line)

    async def run_tool_tree(self, line):
        data = self.tool_picker.determine_tools_and_query(line)
        print(data)
