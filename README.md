# Human Intelligence vs Artificial Intelligence

A working Streamlit web app that runs on a laptop and can be opened on other devices on the same Wi-Fi network.

## Requirements
- Python 3.10 or newer
- Internet is not required for the game logic; the app uses sample responses. The optional Google Fonts import only affects typography.

## Install and run (Windows)
1. Extract the ZIP to a folder.
2. Install Python 3.10+ from https://www.python.org/downloads/ . During installation, tick **Add Python to PATH**.
3. Open Command Prompt in the extracted folder.
4. Run:

   ```bash
   py -m pip install -r requirements.txt
   py -m streamlit run app.py
   ```

5. A browser tab will open, usually at `http://localhost:8501`.

If `py` does not work, try `python -m pip install -r requirements.txt` and `python -m streamlit run app.py`.

## Open it on another device on the same Wi-Fi
Run this command instead:

```bash
py -m streamlit run app.py --server.address 0.0.0.0
```

On the host computer, find its local IPv4 address with `ipconfig` in Command Prompt. On the other device, visit:

`http://YOUR-COMPUTER-IP:8501`

Both devices must be on the same network, and the host computer must stay on with the app running. A school network may block device-to-device access.

## Features
- Rules/start page and player-name login
- Five emotional scenario questions
- 30-second timer per question
- Human-vs-AI score tally and results review
- Local leaderboard saved in `leaderboard.json`
- Responsive browser layout with pastel blue and sage styling

## Important notes
- The “AI” responses are prewritten examples, not generated live by an AI model. No API key is required.
- The labels are based on writing style for this game and do not prove actual authorship.
- This is a demo login: it asks for a display name, but it does not provide secure accounts or passwords.
- Leaderboard is stored on the computer running the app. If multiple devices connect to the same running host, they use the same leaderboard file.
- This is a prototype suitable for a classroom demonstration, not a production authentication system.
