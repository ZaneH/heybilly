# HeyBilly v2

## Introduction
Welcome to **HeyBilly v2**, your voice-activated assistant. Whether you want to check the weather, play your favorite music, or stay updated with the latest news, HeyBilly listens to your commands and acts fast. It's like having a helpful friend, always ready to assist you with just your voice.

Consider setting up the [Discord bot](https://github.com/ZaneH/heybilly-v2-discord) for more features.

## Features

### Real-Time Insights 🌍
Stay connected to real-time data with HeyBilly's precise updates.
- You: "Hey Billy, could you provide the weather forecast for New York?"
- You: "Hey Billy, I need the latest valuation of Ethereum."
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

## Setup Instructions

Start running HeyBilly v2 by following these steps:

### Repository Acquisition
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

### Installation of Dependencies
Effortlessly equip yourself with the necessary tools:

```bash
pip install -r requirements.txt
```

### Configuration of Environment Variables
Evolve `.env.sample` into `.env` and meticulously input your distinct API credentials.

### Mastery Through Model Fine-Tuning
Venture to https://platform.openai.com/finetune, refine `gpt-3.5-turbo-1106` with `./fine_tune_data`, and update your `.env` file with your new MODEL_IDs.

### Initiation of RabbitMQ
Facilitate a flawless flow of messages:

```bash
docker run --rm -d --hostname heybilly-v2-rabbit \
            --name heybilly-v2-rabbit \
            -p 15672:15672 -p 5672:5672 \
            rabbitmq:3-management
```

### Activation
Commence your HeyBilly v2 expedition:

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

## Contributions
We invite you to collaborate, innovate, and share in the creation of HeyBilly v2. Your unique contributions foster the advancement of this open-source community.

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