"""
Keyword worker for handling GIF and string responses based on keywords
"""
import random
import re
import datetime
import requests
from io import BytesIO
from PIL import Image, ImageSequence
import hashlib
import discord
from libs.global_vars import VARS
from bin.helpers import Helpers
from bin.artifical_bot import ArtificialBot


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
        # Do not process the bot's own messages to avoid reacting to lucky draw outputs
        if msg.author == self.client.user:
            return False

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
        for word, category in keyword_strings.items():
            if re.search(rf'\b{re.escape(word)}\b', lowered):
                # Special handling for haralampi category - check chat_mode
                if category == 'haralampi':
                    # If chat_mode is True, use AI bot
                    if VARS.chat_mode:
                        try:
                            # Get username (display name or username)
                            username = msg.author.display_name or msg.author.name
                            # Create ArtificialBot instance with username and message content
                            bot_instance = ArtificialBot(username=username, message_content=msg.content)
                            # Get the response asynchronously
                            response_format = await bot_instance.get_response()
                            response = response_format.punny_response

                            # debug
                            if VARS.debug_mode:
                                print(f"Using ArtificialBot for haralampi response to user: {username}")
                                print(f"ArtificialBot response format: {response_format}")
                                print(f"ArtificialBot response: {response}")

                            await msg.channel.send(response)
                            return True
                        except Exception as e:
                            print(f"Error using ArtificialBot for haralampi response: {e}")
                            import traceback
                            traceback.print_exc()
                            # Fallback to a generic message if bot fails
                            await msg.channel.send("В момента съм се наакал... 🤖")
                            return True
                    else:
                        # chat_mode is False, use database responses
                        counter = self.response_counters[category]
                        responses = getattr(self, f"{category}_responses")
                        response = responses[counter % len(responses)]
                        self.response_counters[category] = (counter + 1) % len(responses)
                        await msg.channel.send(response)
                        return True
                else:
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
                # Anti-spam check
                if not Helpers.anti_spam_check(self.last_message_delta, self.last_message_date):
                    return False

                gif_url = random.choice(gif_list)
                await self._process_and_send_gif(msg, gif_url, word)
                Helpers.last_message(self)
                return True

        return False

    async def _process_and_send_gif(self, msg, gif_url, word):
        """Process, resize and cache GIF in DB, then send it"""
        # Build a deterministic cache filename based on keyword and URL hash
        url_hash = hashlib.md5(gif_url.encode('utf-8')).hexdigest()
        filename = f'{word}_{url_hash}.gif'

        # Local import to avoid circular deps
        from bin.db_helpers import DBHelpers

        # Try to fetch from DB cache
        cached = DBHelpers.fetch_one(
            "SELECT gif_data, mime_type, size_bytes FROM gif_cache WHERE filename = %s LIMIT 1",
            (filename,)
        )
        if cached:
            gif_data, mime_type, size_bytes = cached
            try:
                await msg.channel.send(file=discord.File(fp=BytesIO(gif_data), filename=filename))
                return
            except Exception as e:
                print(f"Failed to send cached GIF {filename}: {e}")
                # fall through to re-fetch/process

        # Not cached or failed to send; fetch, process, cache and send
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
            # Write processed GIF to memory buffer
            buf = BytesIO()
            frames[0].save(
                buf,
                format='GIF',
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=original_gif.info.get('duration', 40),
                disposal=2,
                transparency=original_gif.info.get('transparency', 0)
            )
            gif_bytes = buf.getvalue()
            # Cache in DB
            try:
                DBHelpers.execute(
                    "INSERT INTO gif_cache (filename, mime_type, size_bytes, gif_data) VALUES (%s, %s, %s, %s)",
                    (filename, 'image/gif', len(gif_bytes), gif_bytes)
                )
            except Exception as e:
                print(f"Failed to insert GIF into cache {filename}: {e}")
            # Send to channel
            await msg.channel.send(file=discord.File(fp=BytesIO(gif_bytes), filename=filename))
        except Exception as e:
            print(f"GIF processing error for {word}: {e}")
            await msg.channel.send(gif_url)

    async def handle_keyword_commands(self, msg):
        """Handle keyword-related commands like $key_words and $ChatMode"""

        if msg.content.startswith("$ChatMode"):
            # Toggle chat_mode
            VARS.chat_mode = not VARS.chat_mode
            mode_status = ''
            if VARS.chat_mode:
                mode_status = 'Аз мога да гуворя!'
            else:
                mode_status = 'Деба'
            await msg.channel.send(mode_status)
            return True

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
