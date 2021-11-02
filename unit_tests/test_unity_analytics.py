#!/usr/bin/env python3

import unittest
import unittest.mock as mock

import json
from unity_analytics import unity_analytics

class TestUnityAnalytics(unittest.TestCase):

    def test_init(self):

        input_list = [
            (
                [{"n1": "v1"}, {"n2": "v2"}], 
                [["n1", "n2", "n3"], ["v1", "v2", None]]
            )
        ]

        for data, tbl in input_list:
            with mock.patch.object(unity_analytics, "preprocess_input_txt", return_value=data):
                with mock.patch.object(unity_analytics, "flatten_data", return_value=tbl):
                    analytic = unity_analytics("")
            self.assertEqual(analytic._unity_analytics__data, data)
            self.assertEqual(analytic._unity_analytics__tbl, tbl)

    def test_convert_timestamp(self):

        input_list = [
            (
                [["n1", "n2", "n3", "n4", "n5", "n6"], ["v1", None, True, False, 0, 1.1]], 
                ["n5"], 
                [["n1", "n2", "n3", "n4", "n5", "n6"], ["v1", None, True, False, "1970-01-01 00:00:00", 1.1]]
            ), 
            (
                [["n1", "n2", "n3"], ["v1", 1609459200, 2147483647]], 
                ["n3", "n2"], 
                [["n1", "n2", "n3"], ["v1", "2021-01-01 00:00:00", "2038-01-19 03:14:07"]]
            ), 
            (
                [["n1", "n2", "n3"], [1609459200000, 1609459200000000, 1609459200000000000]], 
                ["n1", "n2", "n3"], 
                [["n1", "n2", "n3"], ["2021-01-01 00:00:00", "2021-01-01 00:00:00", "2021-01-01 00:00:00"]]
            ), 
            (
                [["n"], [1609459200000000000000]], ["n"], ValueError
            ), 
            (
                [["n"], [9999999999999999999999999999]], ["n"], OverflowError
            ), 
            (
                [["n"], [999999999999999999999999999]], ["n"], OSError
            ),
            (
                [["n"], ["Not a timestamp"]], ["n"], TypeError
            ), 
            (
                [["n"], [1]], ["Not exist"], KeyError
            )
        ]

        for tbl, titles, tbl_ in input_list:
            with mock.patch.object(unity_analytics, "preprocess_input_txt", return_value=""):
                with mock.patch.object(unity_analytics, "flatten_data", return_value=tbl):
                    analytic = unity_analytics("")
            if isinstance(tbl_, type) and issubclass(tbl_, BaseException):
                with self.assertRaises(tbl_):
                    analytic.convert_timestamp(titles)
            else:
                analytic.convert_timestamp(titles)
                self.assertEqual(analytic._unity_analytics__tbl, tbl_)

    def test_to_csv(self):

        input_list = [
            (
                [["n1", "n2", "n3", "n4", "n5", "n6"], ["v1", None, True, False, 1, 1.1]], 
                "\"n1\",\"n2\",\"n3\",\"n4\",\"n5\",\"n6\"\r\n\"v1\",\"\",\"True\",\"False\",\"1\",\"1.1\"\r\n"
            )
        ]

        for tbl, csv in input_list:
            with mock.patch.object(unity_analytics, "preprocess_input_txt", return_value=""):
                with mock.patch.object(unity_analytics, "flatten_data", return_value=tbl):
                    analytic = unity_analytics("")
            self.assertEqual(analytic.to_csv(), csv)

    def test_preprocess_input_txt(self):

        input_list = [
            (
                "{\"n1\":\"v1\",\"n2\":\"v2\"}\n{\"n3\":\"v3\"}", 
                [{"n1": "v1", "n2": "v2"}, {"n3": "v3"}]
            ), 
            (
                "{\"n1\":\"v1\",\"n2\":\"v2\"}\n{\"n3\":\"v3\"}\n", 
                [{"n1": "v1", "n2": "v2"}, {"n3": "v3"}]
            ), 
            (
                "{\"n1\":\"v1,\"n2\":\"v2\"}\n{\"n3\":\"v3\"}", 
                # error
            )
        ]

        for input_ in input_list:
            if len(input_) == 1:
                with self.assertRaises(json.JSONDecodeError):
                    unity_analytics.preprocess_input_txt(input_[0])
            else:
                self.assertEqual(unity_analytics.preprocess_input_txt(input_[0]), input_[1])

    def test_flatten_data(self):

        input_list = [
            (
                [
                    {"n1": "v1", "n2": "v2"}, 
                    {"n3": "v3"}
                ], 
                [
                    ["n1", "n2", "n3"], 
                    ["v1", "v2", None], 
                    [None, None, "v3"]
                ]
            ), 
            (
                [
                    {"n1": "v1", "n2": ["a", "b"]}
                ], 
                # error
            ), 
            (
                [
                    {"name": "gameOver", "ts": 12, "debug_device": True, "custom_params": {"gameDuration": 3.6, "Winner": None}, "type": False}, 
                    {"name": "goodGame", "custom_params": {"Player": "?", "currentHP": "100"}, ".": 0, "type": "Unknown"}
                ], 
                [
                    ["name", "ts", "debug_device", "custom_params.gameDuration", "custom_params.Winner", "type", "custom_params.Player", "custom_params.currentHP", ".."], 
                    ["gameOver", 12, True, 3.6, None, False, None, None, None], 
                    ["goodGame", None, None, None, None, "Unknown", "?", "100", 0]
                ]
            )
        ]

        for input_ in input_list:
            if len(input_) == 1:
                with self.assertRaises(ValueError):
                    unity_analytics.flatten_data(input_[0])
            else:
                self.assertEqual(unity_analytics.flatten_data(input_[0]), input_[1])
