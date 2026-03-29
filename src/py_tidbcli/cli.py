import argparse
import sys
import ssl

import pymysql


def parse_args():
    parser = argparse.ArgumentParser(
        prog="ticli",
        description="Simple MySQL/TiDB CLI client using PyMySQL",
        add_help=False,
    )
    parser.add_argument("-i", "--help", action="help", default=argparse.SUPPRESS, help="Display this help message and exit")
    parser.add_argument("-h", "--host", default="127.0.0.1", dest="host", help="Host to connect to (default: 127.0.0.1)")
    parser.add_argument("-P", "--port", type=int, default=4000, dest="port", help="Port number (default: 4000)")
    parser.add_argument("-u", "--user", default="root", dest="user", help="User name (default: root)")
    parser.add_argument("-p", "--password", default="", dest="password", help="Password")
    parser.add_argument("--skip-ssl", action="store_true", help="Disable TLS connection")
    parser.add_argument("-D", "--database", default="test", dest="database", help="Database to use (default: test)")
    parser.add_argument("-e", "--execute", default=None, dest="execute", help="Execute SQL statement and exit")
    return parser.parse_args()


def connect(args):
    ssl_ctx = None
    if not args.skip_ssl:
        ssl_ctx = ssl.create_default_context()

    return pymysql.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
        ssl=ssl_ctx,
        autocommit=True,
    )


def format_result(cursor):
    if cursor.description is None:
        print(f"Query OK, {cursor.rowcount} row(s) affected")
        return

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    if not rows:
        print("Empty set")
        return

    # Calculate column widths
    widths = [len(c) for c in columns]
    str_rows = []
    for row in rows:
        str_row = [str(v) if v is not None else "NULL" for v in row]
        str_rows.append(str_row)
        for i, v in enumerate(str_row):
            widths[i] = max(widths[i], len(v))

    # Print header
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    header = "|" + "|".join(f" {c:<{widths[i]}} " for i, c in enumerate(columns)) + "|"
    print(sep)
    print(header)
    print(sep)

    # Print rows
    for str_row in str_rows:
        line = "|" + "|".join(f" {v:<{widths[i]}} " for i, v in enumerate(str_row)) + "|"
        print(line)
    print(sep)
    print(f"{len(rows)} row(s) in set")


def repl(conn):
    prompt = "mysql> "
    continuation = "    -> "
    buffer = []

    while True:
        try:
            line = input(prompt if not buffer else continuation)
        except (EOFError, KeyboardInterrupt):
            print("\nBye")
            break

        stripped = line.strip()
        if not stripped and not buffer:
            continue

        # Handle quit/exit
        if not buffer and stripped.lower() in ("quit", "exit", "\\q"):
            print("Bye")
            break

        buffer.append(line)
        joined = " ".join(buffer).strip()

        # Execute when statement ends with semicolon
        if joined.endswith(";"):
            sql = joined[:-1].strip()
            if sql:
                try:
                    with conn.cursor() as cursor:
                        cursor.execute(sql)
                        format_result(cursor)
                except pymysql.Error as e:
                    print(f"ERROR {e.args[0]}: {e.args[1]}")
            buffer.clear()


def main():
    args = parse_args()

    try:
        conn = connect(args)
    except pymysql.Error as e:
        print(f"ERROR: Cannot connect to server: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Connected to {args.host}:{args.port}")

    try:
        if args.execute:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(args.execute)
                    format_result(cursor)
            except pymysql.Error as e:
                print(f"ERROR {e.args[0]}: {e.args[1]}")
                sys.exit(1)
        else:
            repl(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
