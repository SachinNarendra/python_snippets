import argparse
import ast
import subprocess
import sys
import time

from qt4 import QtCore, QtGui


class SubprocessThread(QtCore.QThread):
	"""Abstract Class to run a subprocess with
	"""
	def __init__(self, sp_cmd, sp_input, post_process_signal):
		"""Init method."""
		super(SubprocessThread, self).__init__()
		self._subprocess_cmd = sp_cmd
		self._subprocess_input = sp_input
		self._post_process_signal = post_process_signal

	def run(self):
		"""Run the thread."""
		try:
			subprocess_object = subprocess.Popen(
				self._subprocess_cmd,
				stdin=subprocess.PIPE,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)

			stdout, stderr = subprocess_object.communicate(
				input=self._subprocess_input
			)

			# ast.literal_eval raises an exception if the input isn't a valid
			# Python data type, so the code won't be executed if it's not.
			# This way it's much safer than using the eval function
			output = ast.literal_eval(stdout)
			# output = stdout
			self._post_process_signal.emit(output)

		except subprocess.CalledProcessError as e:
			raise RuntimeError(
				"command '{0}' return with error (code {1}): {2}".format(
					e.cmd,
					e.returncode,
					e.output
				)
			)


# ================================= Test Code =================================
# from character_sheet._core import  update_checker
# update_checker.launch_test_subprocess()

def subprocess_test_func(a, b):
	inputs = [line.rstrip('\n') for line in sys.stdin.readlines()]
	output = str([a, b, str(inputs), time.ctime()])
	sys.stdout.write(output)


class TestSubprocess(QtGui.QTextEdit):
	subprocess_completed_signal = QtCore.Signal(list)

	def __init__(self):
		super(TestSubprocess, self).__init__()
		self._a = 'Aaa'
		self._b = 'Bbb'
		self._timer = QtCore.QTimer()
		self._timer.timeout.connect(self.run_subprocess)
		self._timer_interval_sec = 5
		self._subprocess_thread = None
		self._start_subprocess()
		self.subprocess_completed_signal.connect(self._post_process_hook)

	def run_subprocess(self):
		self._subprocess_thread = SubprocessThread(
			self._subprocess_cmd,
			self._subprocess_input,
			self.subprocess_completed_signal,
		)
		self._subprocess_thread.start()

	def _start_subprocess(self):
		self._timer.start(self._timer_interval_sec * 1000)

	def stop_update_checker(self):
		self._timer.stop()

	@property
	def _subprocess_cmd(self):

		return [
			"python", "-m",
			"python_snippets.threading.timer_based_subprocess",
			"-a{0}".format(self._a),
			"-b{0}".format(self._b),
		]

	@property
	def _subprocess_input(self):
		return '\n'.join([
			"Additional Input C",
			"Additional Input D",
		])

	def _post_process_hook(self, output):
		print 'Running _post_process_hook'
		print output
		self.setText('\n'.join(output))

	def close(self):
		self.stop_update_checker()
		super(TestSubprocess, self).close()


def launch_test_subprocess():
	app = QtGui.QApplication.instance() or QtGui.QApplication([])
	wid = TestSubprocess()
	wid.show()
	app.exec_()

# =============================================================================


if __name__ == "__main__":
	description = [
		"Timer based subprocess",
		"Will need to be executed as a python module as it's not an executable."
	]

	parser = argparse.ArgumentParser(
		description=' '.join(description),
		prog='update-checker'
	)

	parser.add_argument('-a', type=str, help='Arg A')
	parser.add_argument('-b', type=str, help='Arg B')

	args = parser.parse_args()
	subprocess_test_func(args.a, args.b)
