"""
Lucky draw command handler module for the Discord Music Bot
Handles the daily fortune/luck drawing feature for users
"""

import random
import subprocess
from libs.global_vars import VARS


class LuckyDrawHandler(VARS):
    def __init__(self, client):
        super().__init__()
        self.client = client

    async def handle_lucky_draw(self, msg):
        """Handle lucky draw commands and self-aware bot restart"""

        # gives the lucky draw result and logs the user in DB
        async def give_lucky_draw(table: str, user: str):
            # Local import to avoid circular deps
            from bin.db_helpers import DBHelpers
            # Insert record
            DBHelpers.execute(f"INSERT INTO {table} (username) VALUES (%s)", (user,))
            lucky_draw = random.choice(self.lucky_list)
            await msg.channel.send(lucky_draw)

        # Lucky draw command
        if msg.content.startswith('$kysmetche'):
            username = str(msg.author)
            # Local import to avoid circular deps
            from bin.db_helpers import DBHelpers

            # Check if already drawn today
            row = DBHelpers.fetch_one(
                "SELECT 1 FROM draw_data WHERE username = %s AND DATE(added_at) = CURDATE() LIMIT 1",
                (username,)
            )
            already_drawn = bool(row)

            # If already drawn, check reroll status
            already_reroll = False
            if already_drawn and 'reroll' in msg.content:
                row_rr = DBHelpers.fetch_one(
                    "SELECT 1 FROM reroll_data WHERE username = %s AND DATE(added_at) = CURDATE() LIMIT 1",
                    (username,)
                )
                already_reroll = bool(row_rr)

            # didn't draw yet
            if not already_drawn:  # h
                await give_lucky_draw('draw_data', username)

            # drawn and wants to reroll and is able to
            elif already_drawn and 'reroll' in msg.content and not already_reroll:  # h
                await give_lucky_draw('reroll_data', username)

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
