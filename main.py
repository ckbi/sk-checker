import pygame
import requests
import re
import sys
import os
import threading
import colorama 

colorama.init()

def stripecheck(key):
	try:
		response = requests.get('https://api.stripe.com/v1/balance', auth=(key, ''))
		if '"available"' in response.text:
			amount = re.findall(r'"amount": (.*?),', response.text)[0]
			currency = re.findall(r'"currency": "(.*?)"', response.text)[0]
			livemode = re.findall(r'"livemode": (.*?),', response.text)[0]
			if int(amount) < 0:
				print(f'\033[37m[\033[33mLIVE\033[37m] But amount is negative - \033[37m[\033[33m{key}\033[37m]')
				open('N-Live-Keys.txt', 'a').write(key + "|amount:" + amount + "|currency:" + currency + "|livemode:" + livemode + "\n")
			elif int(amount) == 0:
				print(f'\033[37m[\033[33mLIVE\033[37m] But amount is 0 - \033[37m[\033[33m{key}\033[37m]')
				open('Z-Live-Keys.txt', 'a').write(key + "|amount:" + amount + "|currency:" + currency + "|livemode:" + livemode + "\n")
			else:
				print(f'\033[37m[\033[32mLIVE\033[37m] Positive amount - \033[37m[\033[32m{amount}\033[37m] - \033[37m[\033[32m{key}\033[37m]')
				open('Live-Keys.txt', 'a').write(key + "|amount:" + amount + "|currency:" + currency + "|livemode:" + livemode + "\n")
		else:
			print(f'\033[37m[\033[31mDEAD\033[37m] - \033[37m[\033[31m{key}\033[37m]')
	except Exception as E:
		print(f'\033[37m[\033[31mERROR\033[37m] - \033[37m[\033[31m{E}\033[37m]')
		
def main():
	print("""\033[34m\n\t███████╗██╗  ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗\n\t██╔════╝██║ ██╔╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝\n\t███████╗█████╔╝     ██║     ███████║█████╗  ██║     █████╔╝ \n\t╚════██║██╔═██╗     ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ \n\t███████║██║  ██╗    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗\n\t╚══════╝╚═╝  ╚═╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝\n\n\t\t\t\033""")
	threads = []
	if len(sys.argv) != 2:
		try:
			ex = sys.executable.split(os.sep)[-1]
		except IndexError:
			ex = sys.executable
		print(f'\033[37m[\033[31mERROR\033[37m] \033[37mPlease run tool like this : \033[31m{ex} {sys.argv[0]} list.txt')
		sys.exit(1)
	lists = open(sys.argv[1], 'r').read().splitlines()
	for i in lists:
		go = threading.Thread(target=stripecheck, args=(i,))
		threads.append(go)
		go.start()
	for go in threads:
		go.join()

if __name__ == '__main__':
	main()
