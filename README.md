# EncryptionPYDiscord

A Discord bot that can encrypt/decrypt text using a crappy caesar cipher algorithm as per specification.
Optimised Port of [Python Encryption CW](https://github.com/BCDeshiG/Python-Encryption-CW) that I made years ago as coursework.

# Usage

## Main commands
- Default prefix is `e!`.
- `encrypt <text>` generates a key (default length 8) and outputs the cipher.
- `decrypt <key> <text>` decrypts the text using said key.
- `chunk <text>` removes spaces in the text before adding a space every 5 characters (replaces AdvancedEncryption from original).
- `setprefix <prefix>` changes the bot prefix.

## Meme commands
- `bekfast` "What is going on here!"
- `status <text>` changes the bot status.
- `reroll` chooses a random status.
- `echo <text>` outputs whatever text you give it.

# Installation
- Make sure you have the latest version of [discord.py](https://discordpy.readthedocs.io/en/latest/) installed.
- Put bot token in `token.txt` in the same directory as the python script.
- Run the python script.
- Simple as. (If it can't find the token, it will ask you to input it manually).