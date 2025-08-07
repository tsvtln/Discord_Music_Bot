"""
Keyword worker for handling GIF and string responses based on keywords
"""
import random
import os
import re
import datetime
import requests
from io import BytesIO
from PIL import Image, ImageSequence
import hashlib
import discord
from libs.global_vars import VARS


class KeywordWorker(VARS):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.response_counters = {
            'bot': 0,
            'haralampi': 0,
        }

    async def handle_keyword_responses(self, msg):
        """Handle all keyword-based responses (GIFs and strings)"""
        keyword_gifs = {
            'наздраве': self.cheer,
            '1991': ['https://i.pinimg.com/736x/79/b7/84/79b784792d35c304af077ee2e450eea1.jpg'],
            'd1': self.d1,
        }

        keyword_strings = {}

        # Use string keys for gif_groups
        gif_groups = {
            'beer': self.beer_keywords,
            'kur': self.kur_keywords,
            'usl': self.usl_keywords,
            'its_wednesday': self.wednesday_keywords,
            'd1': self.d1_keywords,
            'booba': self.booba_keywords,
        }

        # Loop through gif_groups to map keywords to GIF lists
        for gif_key, keywords in gif_groups.items():
            gif_list = getattr(self, gif_key)
            for word in keywords:
                keyword_gifs[word] = gif_list

        # Optimized group mapping for strings
        string_groups = {}

        keyword_categories = {
            'bot': self.bot_keywords,
            'haralampi': self.haralampi_keywords,
        }

        # Loop through string_groups to map keywords to string responses
        for category, keywords in keyword_categories.items():
            for word in keywords:
                keyword_strings[word] = category

        lowered = msg.content.lower()

        # First, check for string responses
        # for word, response in keyword_strings.items():
        #     if re.search(rf'\b{re.escape(word)}\b', lowered):
        #         await msg.channel.send(response)
        #         return True
        for word, category in keyword_strings.items():
            if re.search(rf'\b{re.escape(word)}\b', lowered):
                # Get current counter value for this category
                counter = self.response_counters[category]
                # Get appropriate response array
                responses = getattr(self, f"{category}_responses")
                response = responses[counter % len(responses)]
                # Increment counter for next time
                self.response_counters[category] = (counter + 1) % len(responses)
                await msg.channel.send(response)
                return True

        # Only check for wednesday keywords and respond accordingly if matched
        if any(re.search(rf'\b{re.escape(word)}\b', lowered) for word in self.wednesday_keywords):
            today = datetime.datetime.now().strftime('%A')
            if today.lower() == 'wednesday':
                gif_list = self.its_wednesday
            else:
                gif_list = self.not_wednesday
            gif_url = random.choice(gif_list)
            await self._process_and_send_gif(msg, gif_url, 'wednesday')
            return True

        # Then, check for GIF responses
        for word, gif_list in keyword_gifs.items():
            if re.search(rf'\b{re.escape(word)}\b', lowered):
                gif_url = random.choice(gif_list)
                await self._process_and_send_gif(msg, gif_url, word)
                return True

        return False

    async def _process_and_send_gif(self, msg, gif_url, word):
        """Process, resize and cache GIF, then send it"""
        cache_dir = 'cache/gif_cache'
        os.makedirs(cache_dir, exist_ok=True)
        url_hash = hashlib.md5(gif_url.encode('utf-8')).hexdigest()
        cache_path = os.path.join(cache_dir, f'{word}_{url_hash}.gif')

        if os.path.exists(cache_path):
            await msg.channel.send(file=discord.File(fp=cache_path, filename=f'{word}.gif'))
        else:
            try:
                response = requests.get(gif_url)
                response.raise_for_status()
                original_gif = Image.open(BytesIO(response.content))
                frames = []
                for frame in ImageSequence.Iterator(original_gif):
                    frame = frame.convert('RGBA')
                    frame = frame.resize((120, 120), resample=Image.Resampling.LANCZOS)
                    frame = frame.convert('P', palette=Image.Palette.ADAPTIVE, dither=Image.Dither.FLOYDSTEINBERG)
                    frames.append(frame)
                frames[0].save(cache_path, format='GIF', save_all=True, append_images=frames[1:], loop=0,
                               duration=original_gif.info.get('duration', 40), disposal=2,
                               transparency=original_gif.info.get('transparency', 0))
                await msg.channel.send(file=discord.File(fp=cache_path, filename=f'{word}.gif'))
            except Exception as e:
                print(f"GIF processing error for {word}: {e}")
                await msg.channel.send(gif_url)

    async def handle_keyword_commands(self, msg):
        """Handle keyword-related commands like $key_words"""
        if msg.content.startswith("$key_words"):
            # Build keyword list from all sources
            keyword_gifs = {
                'наздраве': self.cheer,
                '1991': ['https://i.pinimg.com/736x/79/b7/84/79b784792d35c304af077ee2e450eea1.jpg'],
                'd1': self.d1,
            }

            gif_groups = {
                'beer': self.beer_keywords,
                'kur': self.kur_keywords,
                'usl': self.usl_keywords,
                'its_wednesday': self.wednesday_keywords,
                'd1': self.d1_keywords,
                'booba': self.booba_keywords,
            }

            for gif_key, keywords in gif_groups.items():
                gif_list = getattr(self, gif_key)
                for word in keywords:
                    keyword_gifs[word] = gif_list

            all_keywords = set(
                self.beer_keywords +
                self.kur_keywords +
                self.usl_keywords +
                self.bot_keywords +
                self.haralampi_keywords +
                self.wednesday_keywords +
                self.booba_keywords +
                list(keyword_gifs.keys())
            )
            await msg.channel.send(f"Ключови думи:\n{', '.join(sorted(all_keywords))}")
            return True

        return False
