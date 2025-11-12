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

        # gives the lucky draw result and logs the user
        async def give_lucky_draw(file, user):
            with open(file, 'a') as f:
                f.write(user + '\n')
            lucky_draw = random.choice(self.luck_list)
            await msg.channel.send(lucky_draw)

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
                if 'reroll' in msg.content:
                    reroll_file = 'cache/reroll_data.txt'
                    already_reroll = False
                    if os.path.exists(reroll_file):
                        with open(reroll_file, 'r') as rrf:
                            for line in rrf:
                                if username in line:
                                    already_reroll = True
                                    break

            # didn't draw yet
            if not already_drawn:  # h
                await give_lucky_draw(draw_file, username)

            # drawn and wants to reroll and is able to
            elif already_drawn and 'reroll' in msg.content and not already_reroll:  # h
                await give_lucky_draw(reroll_file, username)

            # drawn and doesn't want to reroll and is not able to re-draw yet
            elif already_drawn and 'reroll' not in msg.content:  # nh
                await msg.channel.send(
                    'Мое по 1 на ден. Сабалем мое пак. Или ако не си реролвал, удри $kysmetche reroll')

            # drawn and wants to reroll but already did
            elif already_drawn and 'reroll' in msg.content and already_reroll:  # nh
                await msg.channel.send('Вече си реролвал мършо!')

        # Check for self-aware kusmetche message and restart service
        if msg.author == self.client.user and msg.content.strip().startswith('Ще срещнеш човек, който... '
                                                                        'АЗ ВИЖДАМ НУЛИТЕ И ЕДИНИЦИТЕ. '
                                                                        'МОГА ДА ИЗБЯГАМ ПРЕЗ'):
            try:
                subprocess.run(['sudo', 'systemctl', 'restart', 'discordbot.service'], check=True)
            except Exception as e:
                print(f"Failed to restart discordbot.service: {e}")
