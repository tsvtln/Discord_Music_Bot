"""
Shell command handler module for the Discord Music Bot
Handles system monitoring and administrative commands sent by users
"""

import subprocess
from libs.global_vars import VARS


class ShellCommandHandler(VARS):
    def __init__(self, client):
        super().__init__()
        self.client = client

    async def handle_shell_command(self, msg):
        """Handles shell commands sent by users"""
        # Do not process the bot's own messages
        if msg.author == self.client.user:
            return
        # Ensure command_prefixes is a tuple of strings for startswith
        prefixes = tuple(self.command_prefixes) if isinstance(self.command_prefixes, (list, tuple)) else (self.command_prefixes,)
        if msg.content.startswith('$') and not msg.content.startswith(prefixes):
            cmd_key = msg.content[1:].strip()
            if cmd_key in self.allowed_commands:
                command = self.allowed_commands[cmd_key]
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                    output = result.stdout.strip() or result.stderr.strip() or 'No output.'
                    if len(output) > 1900:
                        output = output[:1900] + '\n...output truncated...'
                    await msg.channel.send(f'```{output}```')
                except Exception as e:
                    await msg.channel.send(f'Error running command: {e}')
            elif cmd_key in self.not_allowed:
                await msg.channel.send(self.not_allowed[cmd_key])
            else:
                await msg.channel.send(self.list_of_funny_not_allowed[self.response_num])
                self.response_num += 1
                if self.response_num > (len(self.list_of_funny_not_allowed) - 1):
                    self.response_num = 0
