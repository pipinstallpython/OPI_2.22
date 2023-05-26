#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import argparse
import sqlite3
import typing as t
from pathlib import Path


def display_ways(waypoints: t.List[t.Dict[str, t.Any]]) -> None:
    """
    Отобразить список маршрутов.
    """
    if waypoints:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 30,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^30} | {:^15} |'.format(
                "№",
                "Название начального маршрута",
                "Название конечного маршрута",
                "Номер маршрута"
            )
        )
        print(line)
        # Вывести данные о всех маршрутах.
        for idx, way in enumerate(waypoints, 1):
            print(
                '| {:>4} | {:<30} | {:<30} | {:>15} |'.format(
                    idx,
                    way.get('start', ''),
                    way.get('finish', ''),
                    way.get('num', 0)
                )
            )
        print(line)
    else:
        print("Cписок пуст")

def create_db(database_path: Path) -> None:
    """
    Создать базу данных.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    # Создать таблицу с информацией о маршрутах.
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS routs (
        routes_id INTEGER PRIMARY KEY AUTOINCREMENT,
        routes_num INTEGER NOT NULL
        )
        """
    )
    # Создать таблицу с информацией о начальных и конечных точках маршрутов
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS waypoints (
        waypoints_id INTEGER PRIMARY KEY AUTOINCREMENT,
        start_way TEXT NOT NULL,
        routes_id INTEGER NOT NULL,
        finish_way TEXT NOT NULL,
        FOREIGN KEY(routes_id) REFERENCES routs(routes_id)
        )
        """
    )
    conn.close()

def add_way(
        database_path: Path,
        start: str,
        finish: str,
        num: int
) -> None:
    """
    Добавить данные о маршрутe.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    # Получить идентификатор маршрута в базе данных.
    # Если такой записи нет, то добавить информацию о новом маршруте.
    cursor.execute(
        """
        SELECT routes_id FROM routs WHERE routes_num = ?
        """,
        (num,)
    )
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            """
            INSERT INTO routs (routes_num) VALUES (?)
            """,
            (num,)
        )
        routes_id = cursor.lastrowid
    else:
        routes_id = row[0]
    # Добавить информацию о новых начальных и конечных точек маршрутов.
    cursor.execute(
        """
        INSERT INTO waypoints (routes_id, start_way, finish_way)
        VALUES (?, ?, ?)
        """,
        (routes_id, start, finish)
    )
    conn.commit()
    conn.close()


def select_all(database_path: Path) -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать все точки маршрутов
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT waypoints.start_way, waypoints.finish_way, routs.routes_num
        FROM waypoints
        INNER JOIN routs ON routs.routes_id = waypoints.routes_id
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "start": row[0],
            "finish": row[1],
            "num": row[2],
        }
        for row in rows
    ]


def find_ways(
        database_path: Path, num: int) \
        -> t.List[t.Dict[str, t.Any]]:
    """
    Выбрать маршрут с данным номером.
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT waypoints.start_way, waypoints.finish_way, routs.routes_num
        FROM waypoints
        INNER JOIN routs ON routs.routes_id = waypoints.routes_id
        WHERE routs.routes_num = ?
        """,
        (num,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "start": row[0],
            "finish": row[1],
            "num": row[2],
        }
        for row in rows
    ]


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "--db",
        action="store",
        required=False,
        default=str(Path.home() / "waypoints.db"),
        help="The database file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("waypoints")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")
    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new way"
    )
    add.add_argument(
        "-s",
        "--start",
        action="store",
        required=True,
        help="Start Route"
    )

    add.add_argument(
        "-f",
        "--finish",
        action="store",
        help="Final Route"
    )

    add.add_argument(
        "-n",
        "--num",
        action="store",
        required=True,
        help="Route number"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all ways"
    )

    # Создать субпарсер для поиска студентов.
    find = subparsers.add_parser(
        "find",
        parents=[file_parser],
        help="find the ways"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Получить путь к файлу базы данных.
    db_path = Path(args.db)
    create_db(db_path)

    # Добавить маршрут.
    if args.command == "add":
        add_way(db_path, args.start, args.finish, args.num)

    # Отобразить все маршруты.
    elif args.command == "display":
        display_ways(select_all(db_path))

    # Выбрать требуемые маршруты.
    elif args.command == "find":
        display_ways(find_ways(db_path, ))
        pass


if __name__ == '__main__':
    main()