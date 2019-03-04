from colorama import Fore, Back, Style	#colored printing
import pprint
pp = pprint.PrettyPrinter(indent=4)

def printPretty(string):
	print(Fore.CYAN)
	pp.pprint(string)
	print(Style.RESET_ALL)

def printError(string):
	print(Fore.RED)
	print(string)
	print(Style.RESET_ALL)

def printGreen(string):
	print(Fore.GREEN)
	print(string)
	print(Style.RESET_ALL)

def printBlue(string):
	print(Fore.BLUE)
	print(string)
	print(Style.RESET_ALL)

def printYellow(string):
	print(Fore.YELLOW)
	print(string)
	print(Style.RESET_ALL)
