import json, os
from time import sleep

class ServerHook:
	def __init__(self, tmux_name, log_path):
		self.tmux_name = tmux_name
		self.log_path = log_path


	def get_log_file(self, lines=1):
		with open(self.log_path, 'r') as logfile:
			logfile_contents = logfile.read().split('\n')
			logfile.close()
		if lines > 1:
			return logfile_contents[-(lines + 1):-2]
		else:
			return logfile_contents[-2]

	def run_command(self, command):
		command = ' Space '.join(command.split(' '))
		prev_output = self.get_log_file()
		os.system(f'tmux send-keys -t {self.tmux_name} {command} Enter')
		output = prev_output
		while output == prev_output:
			output = self.get_log_file()
		return self.get_log_file()

	def get_player_amount(self):
		player_amount = self.run_command('list')
		player_amount = int(player_amount.split('are ')[1].split(' of a max of')[0])
		return player_amount

	def get_players_online(self):
		player_list = self.run_command('list')
		player_list = player_list.split(': ')[2].split(', ')
		return player_list

	def run_title(self, player, text_content, color_content = 'white', bold_content = 'false', italic_content = 'false'):
		self.run_command('title {} title {}\\"text\\":\\"{}\\",\\"color\\":\\"{}\\",\\"bold\\":\\"{}\\",\\"italic\\":\\"{}\\"{}'.format(player, '{', text_content, color_content, bold_content, italic_content, '}'))

	def get_player_pos(self, player):
		player_pos = self.run_command(f'data get entity {player} Pos')
		player_pos = player_pos.split(': ')[2].replace('d', '').strip('[]').split(', ')
		i = 0
		for pos in player_pos:
			player_pos[i] = round(float(pos), 1)
			i += 1
		return player_pos