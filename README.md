# tmuxMCHook

Manipulate a Minecraft Server using Python Code.


## Usage

Must be running on the same machine as the Minecraft Server, and the Minecraft server must be running in a tmux session.


Example code:

```Python
from tmuxMCHook import ServerHook #Import ServerHook from the program.

minecraftserver = ServerHook('tmux_minecraft_session','/home/user/minecraft_server/logs/latest.log') #Create the server hook object.

print(minecraftserver.get_player_amount()) #Get the amount of online players.

minecraftserver.run_title(player = 'Notch', text_content = 'Hello, World!', color_content = 'red', bold_content = 'true', italic_content = 'true') #Run a title on player 'Notch' with the specified settings.

print(minecraftserver.get_players_online()) #List the online players.

print(minecraftserver.get_player_pos('Notch')) #Get the position of player 'Notch'.

print(minecraftserver.run_command('setblock 0 0 0 stone')) #Run the 'Setblock' command.
```

## Known Issues:

Running the same command twice in a row will cause the program to get stuck in an infinite loop.

Lack of features.


## Planned Features:

Multiple colours in one title command.

Subtitle support.

Tellraw function.

Summon function.

Setblock function.

Function to handle entity and block data (like get_player_pos(), but more extensive).
