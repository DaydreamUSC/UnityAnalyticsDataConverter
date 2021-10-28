#!/usr/bin/env python3

import unittest
import unittest.mock as mock

from converter import parse_args, read_input_file, write_output_file

class TestConverter(unittest.TestCase):

    def test_parse_args(self):

        default_output_path = "out.csv"
        input_args_list = [
            ["converter.py", "in.txt", "--output-path", default_output_path], 
            ["converter.py", "in.txt", "-o", default_output_path], 
            ["converter.py", "in.txt", "--output-path", "output.csv"], 
            ["converter.py", "in.txt", "-o", "output.csv"], 
            ["converter.py", "in.txt"]
        ]

        for input_args in input_args_list:
            with mock.patch("sys.argv", input_args):
                ret = parse_args()
            self.assertEqual(len(ret), 2)
            self.assertEqual(ret[0], input_args[1])
            self.assertEqual(ret[1], input_args[3] if len(input_args) > 2 else default_output_path)
    
    def test_read_input_file(self):

        input_list = [
            ("path", "123"), 
            ("\linux\path", "{\"name1\": \"value1\"}\n{\"name2\": \"value2\"}"), 
            ("\linux\path\in.txt", "{\"name\": \"value\"}")
        ]

        for input_path, input_txt in input_list:
            mock_open = mock.mock_open(read_data=input_txt)
            with mock.patch("builtins.open", mock_open):
                ret = read_input_file(input_path)
            mock_open.assert_called_once_with(input_path, "rt", encoding="utf-8", errors="strict")
            self.assertEqual(ret, input_txt)
    
    def test_write_output_file(self):
        
        output_list = [
            ("path", "123"), 
            ("\linux\path", "\"title1\",\"title2\"\r\n\"value1\",\"value2\"\r\n"), 
            ("\linux\path\out.csv", "\"t1\",\"t2\"\r\n\"v1\",\"v2\"")
        ]

        for output_path, output_txt in output_list:
            mock_open = mock.mock_open()
            with mock.patch("builtins.open", mock_open):
                ret = write_output_file(output_path, output_txt)
            mock_open.assert_called_once_with(output_path, "wt", encoding="utf-8", errors="strict")
            mock_open().write.assert_called_once_with(output_txt)
