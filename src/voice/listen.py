import asyncio
import json
import logging
import re
from tenacity import (before_sleep_log, retry, stop_after_attempt,
                      wait_exponential)

from src.graph.builder import GraphBuilder
from src.graph.processor import GraphProcessor
from src.graph.validator import NodeIOValidationError, NodeTypeValidationError
from src.voice.whisper.live_transcribe import LiveTranscribe

# Heavily based on davabase/whisper_real_time for real time transcription
# https://github.com/davabase/whisper_real_time/tree/master

WAKE_WORDS = ["ok billy", "yo billy", "okay billy", "hey billy"]

# Retry logging
logging.basicConfig()
log = logging.getLogger("tenacity.retry")
log.setLevel(logging.INFO)


class Listen():
    def __init__(self, rabbit_client) -> None:
        self.data_queue = asyncio.Queue()
        self.rabbit_client = rabbit_client
        self.builder = GraphBuilder()

        self.live_transcribe = None

    def start(self):
        self.live_transcribe = LiveTranscribe()
        self.live_transcribe.transcribe(self.on_transcription_callback)

    def on_transcription_callback(self, transcript):
        asyncio.run(self.process_transcript(transcript))

    async def process_transcript(self, transcript):
        wake_word_start = self.find_wake_word_start(transcript)
        if wake_word_start == -1:
            return  # No wake word found

        # Slice the line from the first wake word
        # it isn't perfect, but it's good enough
        processed_line = transcript[wake_word_start:]

        # Create and process the graph
        try:
            await self.create_and_process_graph(processed_line)
        except Exception as e:
            logging.error(
                "Error creating and processing graph. Likely a previously unseen request.")
            logging.error(e)

    @retry(wait=wait_exponential(multiplier=1, min=4, max=10),
           stop=stop_after_attempt(3),
           before_sleep=before_sleep_log(log, logging.INFO))
    async def create_and_process_graph(self, processed_line):
        try:
            graph = self.builder.build_graph(processed_line)
            self.rabbit_client.send_ai_response(
                "ai.builder.responses", json.dumps({
                    "input": processed_line,
                    "output": json.loads(graph)
                }, indent=4)
            )

            # GraphProcessor throws a ValueError if the graph is invalid
            processor = GraphProcessor(self.rabbit_client, graph)

            # Attach the request to the processor
            setattr(processor, "user_input", processed_line)

            # Start processing the graph
            await processor.start()

        except NodeIOValidationError:
            logging.error(f"Node IO validation error")
            raise
        except NodeTypeValidationError:
            logging.error(f"Node validation error")
            raise
        except ValueError:
            logging.error(f"Graph validation error")
            raise
        except Exception:
            logging.error("Error creating and processing graph")
            raise

    def stop(self):
        self.should_stop = True

    def find_wake_word_start(self, line):
        normalized_line = line.lower()
        normalized_line = re.sub(r'[^a-zA-Z ]', '', normalized_line)

        wake_word_positions = [normalized_line.find(
            wake_word) for wake_word in WAKE_WORDS if wake_word in normalized_line]
        if not wake_word_positions:
            return -1

        return min(pos for pos in wake_word_positions if pos >= 0)
