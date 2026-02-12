# Telegram Gaming Bot (Hindi)

Yeh ek simple points-based Telegram gaming bot hai.

## Games

- `/toss [amount] [H/T]`
  - Example: `/toss 100 H`
  - Bot random result deta hai:
    - `Heads ✋🏻`
    - `Tails 👌🏻`
  - Agar sahi guess kiya: `+amount`
  - Agar galat hua: `-amount`

- `/hit [1-5]`
  - Example: `/hit 3`
  - Bot random target choose karta hai (1 se 5).
  - Agar sahi laga: `+200 points`
  - Agar galat hua: `-50 points`

## Other Commands

- `/start` - Welcome + guide
- `/help` - Command help
- `/balance` - Current points

## Points System

- Har naya player `1000` points se start karta hai.
- Points memory me store hote hain (bot restart par reset ho jayenge).

## Setup

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
python bot.py
```
