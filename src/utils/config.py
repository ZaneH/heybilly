class CLIArgs:
    discord_tts = False

    # Model selection options
    model = "medium"
    model_directory = None

    # Model caching control options
    model_dir = None
    local_files_only = False

    # Configuration options to control generated outputs
    pretty_json = False
    print_colors = False
    verbose = False

    # Computing configuration options
    device = "auto"
    threads = 0
    device_index = 0
    compute_type = "auto"

    # Algorithm execution options
    language = None
    temperature = 0
    temperature_increment_on_fallback = 0.2
    prompt_reset_on_temperature = 0.5
    best_of = 5
    beam_size = 5
    patience = 1.0
    length_penalty = 1.0
    suppress_blank = True
    suppress_tokens = "-1"
    initial_prompt = None
    condition_on_previous_text = True
    compression_ratio_threshold = 2.4
    logprob_threshold = -1.0
    no_speech_threshold = 0.6
    word_timestamps = False
    prepend_punctuations = "\"'“¿([{-"
    append_punctuations = "\"'.。,，!！?？:：”)]}、"
    repetition_penalty = 1.0
    no_repeat_ngram_size = 0

    # VAD filter arguments
    vad_filter = False
    vad_threshold = None
    vad_min_speech_duration_ms = None
    vad_max_speech_duration_s = None
    vad_min_silence_duration_ms = None

    # Live transcribe options
    live_transcribe = False
    live_volume_threshold = 0.01
    live_input_device = None

    @classmethod
    def update_from_args(cls, args):
        for key, value in vars(args).items():
            if hasattr(cls, key):
                setattr(cls, key, value)
