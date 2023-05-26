#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sqlite3
from ind import create_db, add_way, select_all, find_ways


class TestsRoutes:
    """
    Program test for a list of routes
    """

    def test_create_db(self):
        """
        Checking the database creation.
        """
        database_path = "test.db"
        if Path(database_path).exists():
            Path(database_path).unlink()

        create_db(database_path)
        assert Path(database_path).is_file()
        Path(database_path).unlink()


    def test_add_way(self):
        """
        Checking the addition.
        """
        database_path = "test.db"
        create_db(database_path)
        add_way(database_path, "ppp", "mmm", 20)
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM waypoints
            """
        )
        row = cursor.fetchone()
        assert row == (1, "ppp", 1, "mmm")
        conn.close()
        Path(database_path).unlink()


    def test_select_all(self):
        """
        Checking the selection all.
        """
        database_path = "test.db"
        create_db(database_path)
        add_way(database_path, "ppp", "mmm", 33)
        add_way(database_path, "www", "nnn", 44)

        comparison_output = [
            {"start": "ppp", "finish": 'mmm', "num": 33},
            {"start": "www", "finish": 'nnn', "num": 44},
        ]
        assert select_all(database_path) == comparison_output
        Path(database_path).unlink()


    def test_find_ways(self):
        """
        Checking the selection by routes number
        """
        database_path = "test.db"
        create_db(database_path)
        add_way(database_path, "ppp", "mmm", 33)
        add_way(database_path, "www", "nnn", 44)

        comparison_output = [
            {"start": "ppp", "finish": 'mmm', "num": 33},
        ]
        assert find_ways(database_path, 33) == comparison_output
        Path(database_path).unlink()