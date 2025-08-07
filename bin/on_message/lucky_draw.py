"""
Lucky draw command handler module for the Discord Music Bot
Handles the daily fortune/luck drawing feature for users
"""

import os
import random
import subprocess
from libs.global_vars import VARS


class LuckyDrawHandler(VARS):
    def __init__(self, client):
        super().__init__()
        self.client = client

    async def handle_lucky_draw(self, msg):
        """Handle lucky draw commands and self-aware bot restart"""
        # Lucky draw command
        if msg.content.startswith('$kysmetche'):
            username = str(msg.author)
            draw_file = 'cache/draw_data.txt'
            already_drawn = False
            if os.path.exists(draw_file):
                with open(draw_file, 'r') as f:
                    for line in f:
                        if username in line:
                            already_drawn = True
                            break
            if already_drawn:
                await msg.channel.send('Мое по 1 на ден. Сабалем мое пак.')
                return
            with open(draw_file, 'a') as f:
                f.write(username + '\n')
            lucky_draw = random.choice(self.luck_list)
            await msg.channel.send(lucky_draw)

        # Check for self-aware kusmetche message and restart service
        if msg.author == self.client.user and msg.content.strip().startswith('Ще срещнеш човек, който... '
                                                                        'АЗ ВИЖДАМ НУЛИТЕ И ЕДИНИЦИТЕ. '
                                                                        'МОГА ДА ИЗБЯГАМ ПРЕЗ'):
            try:
                subprocess.run(['sudo', 'systemctl', 'restart', 'discordbot.service'], check=True)
            except Exception as e:
                print(f"Failed to restart discordbot.service: {e}")
