#!/usr/bin/env python3

import argparse

from unity_analytics import unity_analytics

def parse_args():
    """
    Parse the input arguments
    Output:
        Return input_path, output_path, timestamp_titles
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str)
    parser.add_argument("--output-path", "-o", type=str, default="out.csv")
    parser.add_argument("--timestamp-titles", "-t", nargs="*", type=str, default=["ts", "submit_time"])
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    timestamp_titles = args.timestamp_titles

    return input_path, output_path, timestamp_titles

def read_input_file(input_path):
    """
    Read the text file and return its content
    Input: 
        input_path: Path to the text file
    Output:
        Return the content of the text file
    """

    with open(input_path, "rt", encoding="utf-8", errors="strict") as f:
        txt = f.read()
    return txt

def write_output_file(output_path, txt):
    """
    Write the text to the text file
    Input:
        output_path: Path to the text file
        txt: Text to be written into the text file
    Output:
        txt written to the text file
    """

    with open(output_path, "wt", encoding="utf-8", errors="strict") as f:
        f.write(txt)

if __name__ == "__main__":

    input_path, output_path, timestamp_titles = parse_args()

    analytic = unity_analytics(read_input_file(input_path))
    analytic.convert_timestamp(timestamp_titles)
    write_output_file(output_path, analytic.to_csv())
