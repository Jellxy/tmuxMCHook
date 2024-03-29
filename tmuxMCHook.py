import os, subprocess

VERSION = '0.1.1'

class ServerHook:
	def __init__(self, tmux_name):
		self.tmux_name = tmux_name


	def get_log(self, lines = 1):
		if lines > 28:
			raise ValueError('Can only print 28 or less lines of the log.')
		log = subprocess.check_output(['tmux','capture-pane','-S',str(28 - lines),'-p','-t',self.tmux_name]).decode('utf-8').split('\n')
		while '' in log:
			log.remove('')
		return log
		
	def run_command(self, command):
		command = ' Space '.join(command.split(' '))
		prev_output = self.get_log()
		os.system(f'tmux send-keys -t {self.tmux_name} {command} Enter')
		output = prev_output
		while output == prev_output:
			output = self.get_log()
		os.system(f'tmux send-keys -t {self.tmux_name} Enter')
		return output

	def raw_command(self, command):
		command = ' Space '.join(command.split(' '))
		os.system(f'tmux send-keys -t {self.tmux_name} {command} Enter')
		output = self.get_log()
		return output

	def get_player_amount(self):
		player_amount = self.run_command('list')
		player_amount = int(player_amount.split('are ')[1].split(' of a max of')[0])
		return player_amount

	def get_players_online(self):
		player_list = self.run_command('list')
		player_list = player_list.split(': ')[2].split(', ')
		return player_list

	def run_title(self, player, text_content, color_content = 'white', bold_content = 'false', italic_content = 'false'):
		output = self.run_command('title {} title {{\\"text\\":\\"{}\\",\\"color\\":\\"{}\\",\\"bold\\":\\"{}\\",\\"italic\\":\\"{}\\"}}'.format(player, text_content, color_content, bold_content, italic_content))
		return output

	def get_player_pos(self, player):
		player_pos = self.run_command(f'data get entity {player} Pos')
		player_pos = player_pos.split(': ')[2].replace('d', '').strip('[]').split(', ')
		i = 0
		for pos in player_pos:
			player_pos[i] = round(float(pos), 1)
			i += 1
		return player_pos

	def summon_entity(self, entity = 'minecraft:pig', pos = [0,0,0], nbt = ''):
		output = self.run_command('summon {} {} {} {} {}'.format(entity, pos[0], pos[1], pos[2], nbt))
		return output

	def give_player_item(self, player, item = 'minecraft:stone', amount = 1, nbt = ''):
		output = self.run_command('give {} {}{} {}'.format(player, item, nbt, amount))
		return output

	def test_block(self, pos = [0,0,0], block_test = 'minecraft:air'):
		self.raw_command('execute if block {} {} {} {} run summon minecraft:polar_bear 0 -200 0'.format(pos[0], pos[1], pos[2], block_test))
		self.raw_command('execute unless block {} {} {} {} run summon minecraft:bat 0 -200 0'.format(pos[0], pos[1], pos[2], block_test))
		output = self.get_log()
		prev_output = [output, False, False]
		while prev_output[1] == False:
			output = self.get_log()	
			if 'Summoned new ' in output and prev_output[1] == False:
				prev_output[1] = True
		os.system(f'tmux send-keys -t {self.tmux_name} Enter')
		while prev_output[2] == False:
			i = self.get_log()
			if '[HERE]' in i and prev_output[2] == False:
				prev_output[2] = True
		if output.split(': ')[1] == 'Summoned new Polar Bear':
			return True
		elif output.split(': ')[1] == 'Summoned new Bat':
			return False

	def set_block(self, pos = [0,0,0], block = 'minecraft:stone'):
		output = self.raw_command('setblock {} {} {} {}'.format(pos[0], pos[1], pos[2], block))
		return output