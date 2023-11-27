import unittest
from unittest.mock import patch
from gdb.py import (run_gdb_command, parse_gdb_output, read_json_file, write_json_file, main_search_code, remove_safe_functions, combine_data_for_same_function, list_functions, search_function)
from io import StringIO
import json
import os

class Test(unittest.TestCase):

	def test_run_gdb_command_success(self):
		with path('subprocess.check_output') as mocked_check_output:
			mocked_check_output.return_value = b'GDB output'
			result = run_gdb_command('/path/to/binary')
			self.assertEqual(result, 'GDB output')

	def test_run_gdb_command_failure(self):
		with patch('subprocess.check_output') as mocked_check_output:
			mocked_check_output.side_effect = subprocess.CalledProcessError(1, 'gdb')
			with self.assertRaises(SystemExit):
				run_gdb_command('/path/to/binary')

	def test_parse_gdb_output(self):
		sample_output = "0x00000000 main\n0x00000010 helper_function\n"
		expected_result = [
		{"address": "0x00000000", "name": "main", "signature": ""},
		{"address": "0x00000010", "name": "helper_function", "signature": ""}
		]
		self.assertEqual(parse_gdb_output(sample_output), expected_result)

	def test_read_write_json_file(self):
		test_data = [{"test": "data"}]
		test_file = 'test.json'

		write_json_file(test_file, test_data)
		self.assertTrue(os.path.exists(test_file))

		read_data = read_json_file(test_file)
		self.assertEqual(read_data, test_data)

		os.remove(test_file)

	# mock file operations
	# use script name (mine is gdb.py)
	def test_main_search_code(self):
		with patch('gdb.run_gdb_command') as mocked_run, patch('gdb.parse_gdb_output') as mocked_parse, patch('gdb.write_json_file') as mocked_write;
		main_search_code()
		mocked_run.assert_called()
		mocked_parse.assert_called()
		mocked_write.assert_called()

	def test_remove_safe_functions(self):
        with patch('gdb.read_json_file') as mocked_read, patch('gdb.write_json_file') as mocked_write:
            remove_safe_functions()
            mocked_read.assert_called()
            mocked_write.assert_called()

    def test_combine_data_for_the_same_function(self):
        with patch('gdb.read_json_file') as mocked_read, patch('gdb.write_json_file') as mocked_write:
            combine_data_for_the_same_function()
            mocked_read.assert_called()
            mocked_write.assert_called()

    def test_list_functions(self):
        with patch('sys.stdout', new_callable=StringIO) as mocked_output, patch('gdb.read_json_file') as mocked_read:
            mocked_read.return_value = [{"address": "0x00000000", "name": "main"}]
            list_functions()
            self.assertIn("0x00000000: main", mocked_output.getvalue())

    def test_search_function(self):
        with patch('builtins.input', return_value="main"), patch('sys.stdout', new_callable=StringIO) as mocked_output, patch('gdb.read_json_file') as mocked_read:
            mocked_read.return_value = [{"address": "0x00000000", "name": "main"}]
            search_function()
            self.assertIn("found 0x00000000: main", mocked_output.getvalue())

if __name__ == '__main__':
    unittest.main()
