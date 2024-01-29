# HeyBilly v2

## Introduction
Welcome to **HeyBilly v2**, your voice-activated assistant. Whether you want to check the weather, play your favorite music, or stay updated with the latest news, HeyBilly listens to your commands and acts fast. It's like having a helpful friend, always ready to assist you with just your voice.

Consider setting up the [Discord bot](https://github.com/ZaneH/heybilly-v2-discord) for more features.

## Features

### Real-Time Insights 🌍
Stay connected to real-time data with HeyBilly's precise updates.
- You: "Hey Billy, could you provide the weather forecast for New York?"
- You: "Hey Billy, post the price of Ethereum to Discord."
- You: "Hey Billy, post the NFL player with the most touchdowns in Discord."

### Symphony of Sounds 🎵
Dictate your auditory experience with intuitive voice controls.
- You: "Ok Billy, play Lo-Fi music."
- You: "Ok Billy, could you play 'Bohemian Rhapsody' by Queen?"
- You: "Ok Billy, reduce the volume slightly, please."
- You: "Ok Billy, adjust the volume to level 5."
- You: "Ok Billy, pause the playback."

### Portal to Entertainment 🎥
Unlock a world of leisure with an array of engaging commands.
- You: "Yo Billy, post a video featuring pandas to Discord."
- You: "Yo Billy, post a coin toss."
- You: "Yo Billy, provide a random interesting fact."
- You: "Yo Billy, post a comedic GIF to Discord."
- You: "Yo Billy, play crickets sound effect."

### Articulate Interactions 🗣️
Experience dynamic interactions with HeyBilly's advanced Text-to-Speech feature.

- Currently only available for Discord.

## Preview

![Console screenshot](https://github.com/ZaneH/heybilly-v2/assets/8400251/f29cc1ef-b7d5-444a-ba68-211c27aa2a11)

## Setup Instructions

Start running HeyBilly v2 by following these steps:

### Clone Repository
Grab the latest version of HeyBilly right from the source:

```bash
git clone https://github.com/ZaneH/HeyBilly-v2.git
```

### Environment Configuration
Create and activate a conda environment for HeyBilly:

```bash
conda create -n heybilly-v2 python=3.10 -y
conda activate heybilly-v2
```

### Install Dependencies
Install Python packages:

```bash
pip install -r requirements.txt
```

### Configuration of Environment Variables
Evolve `.env.sample` into `.env` and meticulously input your distinct API credentials.

### Train Your Model With Fine-Tuning
Go to https://platform.openai.com/finetune, and create a job for `gpt-3.5-turbo-1106` with each file in `./fine_tune_data`. Update your `.env` file with your new MODEL_IDs once the jobs are complete.

### Run RabbitMQ
Start the RabbitMQ container:

```bash
docker run --rm -d --hostname heybilly-v2-rabbit \
            --name heybilly-v2-rabbit \
            -p 15672:15672 -p 5672:5672 \
            rabbitmq:3-management
```

### Activation
Start HeyBilly v2:

```bash
python main.py # you can add --verbose
```

## Usage
HeyBilly v2 is in a phase of continuous enhancement. Anticipate additional functionalities and updates shortly.

## For Developers 🛠️
HeyBilly v2 is designed with developers in mind. Explore the depths of HeyBilly's architecture, understand its lifecycle, and contribute to its growth:

- [Graph Lifecycle](https://github.com/ZaneH/heybilly-v2/wiki/Graph-Lifecycle)
- [Developer's Guide](https://github.com/ZaneH/heybilly-v2/wiki/Developers-Guide)

We encourage developers to delve into our comprehensive guides and contribute to the evolution of HeyBilly v2.

### Built-in Nodes

HeyBilly v2 is equipped with a diverse set of built-in nodes, each designed to perform specific tasks seamlessly. Here's an overview of the nodes you can utilize within your workflows:

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

#### Multimedia Nodes
- **youtube.play**: Plays a specified YouTube video.
- **sfx.play**: Plays a short sound effect.

#### Utility Nodes
- **volume.set**: Adjusts the volume level of the bot in voice channels.
- **done**: Marks the completion of the workflow in the graph.

These nodes are the building blocks of HeyBilly v2, allowing users to create versatile and interactive voice command workflows. Feel free to create your own nodes and open a PR!

## Contributions
The project is still in its infancy and your contributions would have a big impact. Here are some ways you can contribute:

### Todo:

- [ ] Add more fine-tuning data
- [ ] Play TTS response if the graph fails completely
- [ ] Figure out how the `validate_inputs` function could be useful (currently unused)
- [ ] Improve speed of voice transcription (VAD, etc.)
- [ ] Play TTS through computer if the user doesn't want to use the Discord bot
- [ ] Add more built-in nodes (Decision node, etc.)
- [ ] ~~Add user_text_prompt node~~ (In progress)
- [ ] Feed previous request into next request (e.g. "What is the weather in New York?" -> "What about the time?")

#### Low Priority

- [ ] Create tooling for graphs to aid in inspection and fine-tuning

### Contribution Process
1. Fork the Repository
2. Establish Your Feature Branch (`git checkout -b feature/YourInnovativeFeature`)
3. Commit Your Changes (`git commit -m 'Add YourInnovativeFeature'`)
4. Push to the Branch (`git push origin feature/YourInnovativeFeature`)
5. Commence a Pull Request

## License
HeyBilly v2 is licensed under the MIT License. Consult `LICENSE` for complete terms.

## Stay Connected
- Twitter: [@zanehelton](https://twitter.com/zanehelton)
- GitHub URL: [HeyBilly v2 on GitHub](https://github.com/ZaneH/HeyBilly-v2)

---

🌟 Enjoying HeyBilly v2? Show your support with a star!
