import argparse


def module_function():
	print "Calling module_function"


def script_function(arg_a, arg_b):
	print "Calling script_function with following args:"
	print arg_a
	print arg_b
	module_function()


if __name__ == "__main__":
	description = [
		"A simple python file that can work both as a script and a module",
		"Will need to be excuted a python script as it's not an executable."
	]

	parser = argparse.ArgumentParser(
		description=' '.join(description),
		prog='callsheet-update-checker'
	)

	parser.add_argument('-a', type=str, help='Arg A')
	parser.add_argument('-b', type=str, help='Arg B')

	args = parser.parse_args()
	script_function(args.a, args.b)


# Usage Example:
# python -m testing.script_module_combo "-a A" "-b B"

