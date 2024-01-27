# HeyBilly v2 💻🎶

Welcome to **HeyBilly v2**, it's a modular voice assistant. Create your
own integrations, or use the ones that are already built-in. Compose a tweet,
listen to music, or get the weather all with your voice. Contributions are
welcome.

## Features

- **Real-Time Data**: Ask HeyBilly about what's going on in the world 🌎
  - "Hey Billy, what's the weather in Alaska?"
  - "Okay Billy, what's the price of gold?"
- **YouTube DJ**: Play, pause, stop, or resume YouTube videos in voice chat. 🎶
  - "Yo Billy, play Lo-Fi music."
  - "Hey Billy, play Let It Be by The Beatles."
  - "Hey Billy, turn the volume down."
  - "Okay Billy, set the volume to 4."
  - "Okay Billy, pause music."
- **Fun Commands**: Videos, GIFs, and coin flips are just a voice command away. 🎲🎥
  - "Yo Billy, post a video of a cat."
  - "Hey Billy, post a coin flip to the Discord."
  - "Hey Billy, post a random number."
  - "Okay, Billy, post a funny GIF."
  - "Hey Billy, play a cricket sound."
  - "Hey Billy, post a scary movie trailer."
- **Text-to-Speech (TTS) Support**: HeyBilly can speak in the voice chat, making your interactions even more dynamic. 🗣️

## Getting Started

Follow these steps to get HeyBilly up and running on your Discord server:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ZaneH/HeyBilly-v2.git
   ```

2. **Create a Virtual Environment**
   Use Conda to create a new environment specifically for HeyBilly:
   ```bash
   conda create -n heybilly-v2 python=3.10 -y
   ```

3. **Activate the Virtual Environment**
   ```bash
   conda activate heybilly-v2
   ```

4. **Install Dependencies**
   Install all the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```

5. **Setup Environment Variables**
   
   Rename `.env.sample` to `.env` and populate it with your own API keys.

6. **Fine-Tune the Model**
   
   Go to https://platform.openai.com/finetune and create a new fine-tuning job. Use the files in `./fine_tune_data` to train the `gpt-3.5-turbo-1106` model. Once finished, copy the model ID and update your environment variables accordingly.

7. **Run HeyBilly**
   ```bash
   python main.py
   ```

## Usage

This project is under active development. Please check back shortly...

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Twitter - [@zanehelton](https://twitter.com/zanehelton)

Project Link - [https://github.com/ZaneH/HeyBilly-v2](https://github.com/ZaneH/HeyBilly-v2)

---

Give a ⭐️ if you like this project!
