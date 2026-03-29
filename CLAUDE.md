# ticli (py-tidbcli)

Simple MySQL/TiDB CLI client using PyMySQL only.

## Project structure

```
py-tidbcli/
├── pyproject.toml          # Package config, entry point: ticli
├── src/py_tidbcli/
│   ├── __init__.py
│   └── cli.py              # All logic in one file
├── README.md
└── CLAUDE.md
```

## Build & Run

```bash
# Run from source
uv run ticli -h <host> -u <user> -p <password>

# Run via uvx (from local path)
uvx --from . ticli -h <host> -u <user> -p <password>
```

## Design decisions

- **Single dependency**: pymysql[rsa] only. No other DB drivers.
- **TLS by default**: Uses `ssl.create_default_context()`. Disable with `--skip-ssl`.
- **CLI flags mirror mysql**: `-h` host, `-P` port, `-u` user, `-p` password, `-D` database. Help is `-i` (since `-h` is taken by host).
- **Semicolon-terminated execution**: SQL runs when `;` is entered. Multi-line supported.
- **autocommit=True**: No implicit transactions.
- **Default database**: `test`
- **Default port**: `4000` (TiDB default)

## Testing

Use TiDB Cloud Zero for quick integration tests:

```bash
curl -s -X POST https://zero.tidbapi.com/v1alpha1/instances \
  -H 'Content-Type: application/json' -d '{"tag":"ticli-test"}'
```

Then connect with the returned host/user/password.
