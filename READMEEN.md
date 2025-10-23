<h1 align="center">Markdown Channel Bot</h1>

<table>
<tr>
<td width="40%" align="center">
  <img src="https://github.com/crrrowz/MD-Sofrware/blob/main/app.png?raw=true" width="300" />
</td>
<td width="60%" valign="middle">

This is a simple and secure **Telegram bot**, written in **Python**, designed to receive messages formatted in **Markdown**, convert them to **HTML**, and then send them to a specific Telegram channel.  

The bot is **private by design**, meaning it only responds to the owner’s user ID defined in the configuration file.

</td>
</tr>
</table>

---

## ✨ Main Features

- **Private & Secure:** The bot only accepts messages from the user ID defined as `MY_USER_ID` in the config file and ignores all others.  
- **Markdown Conversion:** Automatically converts Markdown formatting (like **Bold**, *Italic*, `code`, ```python```) to the HTML format supported by Telegram.  
- **Channel Posting:** Instantly sends the formatted message to your selected channel (`CHANNEL_ID`).  
- **Hot Reload:** The bot re-reads `config.json` before every message, so you can update `CHANNEL_ID` or `MY_USER_ID` without restarting the bot!  
- **Error Handling:** Includes handling for common issues such as:
  - Missing or empty `config.json` file.  
  - Invalid `BOT_TOKEN`.  
  - Incorrect `CHANNEL_ID` or missing admin permissions for the bot in the channel.  

---

## ⚙️ Installation & Setup

### 1. Requirements

Make sure you have the required libraries installed:

```bash
pip install python-telegram-bot chatgpt-md-converter
```

### 2. Create the config.json file

In the same folder as your bot code, create a file named `config.json` with the following content:

```json
{
  "BOT_TOKEN": "your_bot_token_from_BotFather",
  "CHANNEL_ID": "@username_of_your_channel",
  "MY_USER_ID": ""
}
```

**Explanation:**  
- `BOT_TOKEN`: Obtain it from [@BotFather](https://t.me/BotFather) on Telegram.  
- `CHANNEL_ID`: The username (like `@my_channel`) or numeric ID (e.g. `-100123456`) of your Telegram channel.  
- `MY_USER_ID`: Leave this empty at first (`""`).  

---

### 3. Run the Bot & Get Your User ID

Start the bot for the first time:

```bash
python bot.py
```

Then open the bot on Telegram and send it any message (e.g., "Hello").  
The bot will fail to send but reply with a message like:

```
Set 123456789 in MY_USER_ID to restrict access
```

This number will also appear in the terminal.

---

### 4. Update the Configuration

1. Copy the number (your Telegram user ID).  
2. Paste it into the `MY_USER_ID` field in `config.json`.  
3. Save the file — **no need to restart the bot!**

---

### 5. Usage

You’re now ready. Send any Markdown-formatted message to your bot, and it will both reply with the formatted version and post it directly to your Telegram channel.

---

## 🧩 (Optional) Convert to Executable (EXE)

To make the bot run as a standalone Windows program without manually launching Python:

1. Install pyinstaller:

```bash
pip install pyinstaller
```

2. Build the executable (optionally include an icon `app.ico`):

```bash
pyinstaller --onefile --icon=app.ico --hidden-import=telegram.warnings bot.py
```

3. A new folder named **dist** will appear containing your ready-to-use executable file.
