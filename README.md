# VCFighter (Bot + Userbot)

## Architecture
- Controller Bot → commands
- Userbot → VC join + audio relay

## Commands (Control Group)
/connect <group_id>
/volume <0-300>
/stop

## Requirements
- Python 3.9+
- ffmpeg
- Userbot admin (Manage VC) in target group

## Run
python3 controller_bot/bot.py
python3 worker_userbot/main.py
