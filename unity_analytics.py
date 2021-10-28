#!/usr/bin/env python3

import json

class unity_analytics():
    """
    Contains the Unity Analytics raw data output dump
    """

    def __init__(self, input_txt):
        """
        Initialize the object
        Input: 
            input_txt: Raw text output from Unity Analytics, in JSON format
        Output:
            Raise JSONDecodeError if input_txt cannot be understood
        """
        
        self.__data = self.preprocess_input_txt(input_txt)
        self.__tbl = self.flatten_data(self.__data)

    def to_csv(self):
        """
        Return the CSV of the data, according to RFC 4180
        """

        csv = ""
        for row in self.__tbl:
            for cell in row:
                cell_ = "" if cell == None else str(cell)
                csv += "\"" + cell_.replace("\"", "\"\"") + "\","
            csv = csv[:-1]
            csv += "\r\n"
        return csv

    @staticmethod
    def preprocess_input_txt(input_txt):
        """
        Convert the JSON input into Python builtin object
        Input: 
            input_txt: Raw text output from Unity Analytics, in JSON format
        Output: 
            Return the object of the input_txt
            Raise JSONDecodeError if input_txt cannot be understood
        """

        data = []
        txt_row = input_txt.split("\n")
        for json_str in txt_row:
            if len(json_str) > 0:
                data.append(json.loads(json_str))
        return data

    @classmethod
    def flatten_data(cls, data):
        """
        Convert a JSON like object into a table
        Input:
            data: List of dict, str, int, float, True, False, or None
        Output:
            Return 2D list, 1st row contains titles, remaining are flatten data
            Raise ValueError if data cannot be understood
        """

        tbl_dict = {}
        for i in range(len(data)):
            cls.__flatten_data_traverse(data[i], tbl_dict, i, "")

        tbl = [[]]
        for key, value in tbl_dict.items():
            tbl[0].append(key)
            if len(value) < len(data):
                value.extend([None for i in range(len(data) - len(value))])
        for i in range(len(data)):
            tbl.append([tbl_dict[key][i] for key in tbl[0]])

        return tbl
    
    @classmethod
    def __flatten_data_traverse(cls, data, tbl, depth, prefix):
        """
        Traverse and add to dict of the same row
        """

        if isinstance(data, dict):
            for key, value in data.items():
                next_prefix = str(key).replace(".", "..")
                if len(prefix) > 0:
                    next_prefix = prefix + "." + next_prefix
                cls.__flatten_data_traverse(value, tbl, depth, next_prefix)
        else:
            if not (isinstance(data, str) or isinstance(data, int) or isinstance(data, float) or 
                    data == True or data == False or data == None):
                raise ValueError()
            if prefix not in tbl:
                tbl[prefix] = []
            if len(tbl[prefix]) < depth:
                tbl[prefix].extend([None for i in range(depth - len(tbl[prefix]))])
            tbl[prefix].append(data)
