# HeyBilly

## Introduction
Welcome to **HeyBilly**, your voice-activated assistant. Whether you want to check the weather, play your favorite music, or stay updated with the latest news, HeyBilly listens to your commands and acts fast. It's like having a helpful friend, always ready to assist you with just your voice.

Consider setting up the [Discord bot](https://github.com/ZaneH/heybilly-discord) for more features.

## Features

### Real-Time Insights 🌍
Stay connected to real-time data with HeyBilly's precise updates.
- You: "Hey Billy, could you provide the weather forecast for New York?"
- You: "Hey Billy, post the price of Ethereum to Discord."
- You: "Hey Billy, post the NFL player with the most touchdowns in Discord."
- You: "Hey Billy, post the top stories from Hacker News to Discord."

### Symphony of Sounds 🎵
Dictate your auditory experience with intuitive voice controls.
- You: "Ok Billy, play Lo-Fi music."
- You: "Ok Billy, could you play 'Hotel California' by The Eagles?"
- You: "Ok Billy, reduce the volume slightly, please."
- You: "Ok Billy, adjust the volume to level 5."
- You: "Ok Billy, pause the music."

### Portal to Entertainment 🎥
Unlock a world of leisure with an array of engaging commands.
- You: "Yo Billy, post a video featuring pandas to Discord."
- You: "Yo Billy, post a coin toss."
- You: "Yo Billy, provide a random interesting fact."
- You: "Yo Billy, post a comedic GIF to Discord."
- You: "Yo Billy, play crickets sound effect."

### Articulate Interactions 🗣️
Experience dynamic interactions with HeyBilly's advanced Text-to-Speech feature.
You have the option to play TTS through your computer's audio (default) or
through the Discord bot.
- **Note:** FFmpeg is required to play TTS through your computer's audio.

## Preview

![Console screenshot](https://github.com/ZaneH/heybilly/assets/8400251/f29cc1ef-b7d5-444a-ba68-211c27aa2a11)

## Setup Instructions

Start running HeyBilly by following these steps:

### Clone Repository
Grab the latest version of HeyBilly right from the source:

```bash
git clone https://github.com/ZaneH/HeyBilly.git
```

### Environment Configuration
Create and activate a conda environment for HeyBilly:

```bash
conda create -n heybilly python=3.10 -y
conda activate heybilly
```

### Install Dependencies
Install Python packages:

```bash
pip install -r requirements.txt
```

### Train Your Model With Fine-Tuning
Go to https://platform.openai.com/finetune, and create a job for `gpt-3.5-turbo-1106` with each file in `./fine_tune_data`. Update your `.env` file with your new MODEL_IDs once the jobs are complete.

### Configuration of Environment Variables
Move `.env.sample` to `.env` and fill in the necessary values. You'll need the fine-tuned model IDs from the previous step.

### Run RabbitMQ
Start the RabbitMQ container:

```bash
make rabbitmq
```

### Start HeyBilly

```bash
make start # starts HeyBilly
make help # shows options
```

## Usage

Run the `main.py` script with optional flags to customize behavior:

- **Help:** `python main.py --help`
- **Verbose Logging:** `python main.py --verbose true` (provides detailed logs)
- **Discord Text-to-Speech:** `python main.py --discord-tts true` (plays TTS through Discord; defaults to computer audio if omitted)

Combine flags as needed, e.g., `python main.py --verbose true --discord-tts true`.

## For Developers 🛠️
HeyBilly is designed with developers in mind. Explore the depths of HeyBilly's architecture, understand the "graph lifecycle", and contribute to its growth:

- [Graph Lifecycle](https://github.com/ZaneH/heybilly/wiki/Graph-Lifecycle)
- [Developer's Guide](https://github.com/ZaneH/heybilly/wiki/Developers-Guide)

### Built-in Nodes

HeyBilly is equipped with a diverse set of built-in nodes, each designed to perform specific tasks seamlessly. Here's an overview of the nodes you can utilize within your workflows:

#### Input & Output Nodes
- **input.voice**: Captures voice commands from the user.
- **user_text_prompt**: **(Not implemented)** Prompts the user for text input.
- **output.tts**: Converts text into spoken voice in the chat.

#### Social Media & Communication Nodes
- **twitter.post**: **(Not implemented)** Posts messages to Twitter.
- **discord.post**: Sends messages or content to Discord channels.

#### Query Nodes
- **wolfram.simple**: Fetches and provides data from Wolfram Alpha, including weather, stocks, and more.
- **hn.top**: Retrieves top stories from Hacker News.
- **nyt.top**: Retrieves top stories from the New York Times.
- **giphy.search**: Finds and posts GIFs based on specified search criteria.
- **youtube.search**: Searches for YouTube videos based on user queries.
- **pexels.search**: Searches for images via the Pexels API.
- **tradingview.chart**: Fetches trading charts from TradingView.

#### Multimedia Nodes
- **music.control**: Controls the playback of music.
- **sfx.play**: Plays a short sound effect.

#### Utility Nodes
- **volume.set**: Adjusts the volume level of the bot in voice channels.
- **done**: Marks the completion of the workflow in the graph.

These nodes are the building blocks of HeyBilly, allowing users to create versatile and interactive voice command workflows. Feel free to create your own nodes and open a PR!

## Contributions
The project is still in its infancy and your contributions would have a big impact. Here are some ways you can contribute:

### Todo:

- [ ] Add more fine-tuning data
- [ ] Play TTS response if the graph fails completely
- [ ] Figure out how the `validate_inputs` function could be useful (currently unused)
- [ ] Add more built-in nodes (Decision node, etc.)
- [ ] ~~Add user_text_prompt node~~ (In progress)
- [ ] Feed previous request into next request (e.g. "What is the weather in New York?" -> "What about the time?")
- [ ] Separate Rabbit data from RAG data
- [x] Improve speed of voice transcription (VAD, etc.)
- [x] Play TTS through computer if the user doesn't want to use the Discord bot
- [x] Create tooling for graphs to aid in inspection and fine-tuning
  - [Tool link](https://graph.zaaane.com/)

### Contribution Process
1. Fork the Repository
2. Establish Your Feature Branch (`git checkout -b feature/YourInnovativeFeature`)
3. Commit Your Changes (`git commit -m 'Add YourInnovativeFeature'`)
4. Push to the Branch (`git push origin feature/YourInnovativeFeature`)
5. Commence a Pull Request

## License
HeyBilly is licensed under the MIT License. Consult `LICENSE` for complete terms.

## Stay Connected
- Twitter: [@zanehelton](https://twitter.com/zanehelton)
- GitHub URL: [HeyBilly on GitHub](https://github.com/ZaneH/HeyBilly)

---

🌟 Enjoying HeyBilly? Show your support with a star!
