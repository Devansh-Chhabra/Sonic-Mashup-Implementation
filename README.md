# 🎵 SonicMash CLI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-v2023-red?style=flat-square&logo=youtube&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**A High-Performance Command Line Tool for Audio Mashups**

Automated audio processing that fetches, cuts, and merges tracks from YouTube.

---

## 📖 Overview

**SonicMash CLI** is a Python script that automates the creation of music mashups. It performs the following steps automatically:

1. **Search & Download:** Fetches random tracks of a specified singer from SoundCloud (bypassing geo-blocks).
2. **Audio Processing:** Trims a random clip from each track to your desired duration.
3. **Merging:** Stitches all clips together into a single, seamless `.mp3` file.



---

## 🛠️ Local Installation

Follow these steps to run the application on your local machine.

### 1. Clone the Repository

```bash
git clone https://github.com/Devansh-Chhabra/Sonic-Mashup-Web-Service
cd Sonic-Mashup-Web-Service
```

### 2. Install Dependencies

Make sure you have Python installed. Then run:

```bash
pip install -r requirements.txt
```
### 3. Setup Environment Variables

To enable the email feature, you must create a `.env` file in the root directory.

Create a file named `.env` and add the following:

```ini
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_16_char_app_password
```

**Note:** For Gmail, you must use an App Password, not your regular login password. [Learn how to create one here](https://support.google.com/accounts/answer/185833).

### 4. Run the App

Launch the Streamlit server:

```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

---

## 🖥️ Usage

### Command Line (CLI)
You can run the logic script independently in your terminal.

**Syntax:**
```bash
python 102317041.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>
```

---

## 📦 Dependencies

- `streamlit`: For the web interface.
- `pydub` & `ffmpeg`: For audio processing.
- `yt-dlp`: For scraping
- `python-dotenv`: For managing secure credentials.

---


## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Devansh Chhabra**  
📧 Email: [devanshchhabr@gmail.com](mailto:devanshchhabr@gmail.com)  

---
