# ticli

A simple MySQL/TiDB CLI client using PyMySQL. Connects with TLS by default.

## Install & Run

```bash
# Run directly with uvx (no install needed)
uvx --from git+https://github.com/bohnen/py-tidbcli ticli -h <host> -u <user> -p <password>

# Install as a persistent tool with uv
uv tool install git+https://github.com/bohnen/py-tidbcli
ticli -h <host> -u <user> -p <password>

# Or install with pip
pip install git+https://github.com/bohnen/py-tidbcli
ticli -h <host> -u <user> -p <password>
```

## Options

| Option | Description | Default |
|---|---|---|
| `-h`, `--host` | Server hostname | `127.0.0.1` |
| `-P`, `--port` | Port number | `4000` |
| `-u`, `--user` | Username | `root` |
| `-p`, `--password` | Password | (empty) |
| `-D`, `--database` | Database to use | `test` |
| `--skip-ssl` | Disable TLS | TLS enabled |
| `-i`, `--help` | Display help | |

## Usage

### Connect to TiDB Cloud

```bash
ticli -h gateway01.us-west-2.prod.aws.tidbcloud.com -P 4000 -u 'user.root' -p 'password'
```

### Connect to local MySQL/TiDB

```bash
ticli -h 127.0.0.1 -P 4000 -u root --skip-ssl
```

### Interactive session

```
Connected to gateway01.us-west-2.prod.aws.tidbcloud.com:4000
mysql> SELECT VERSION();
+-------------------------------+
| VERSION()                     |
+-------------------------------+
| 8.0.11-TiDB-v8.5.3-serverless |
+-------------------------------+
1 row(s) in set
mysql> quit
Bye
```

### Pipe SQL from stdin

```bash
echo "SELECT 1+1 AS result;" | ticli -h <host> -u <user> -p <password>
```

## Commands

| Command | Description |
|---|---|
| `quit`, `exit`, `\q` | Exit the client |

Statements are executed when terminated with `;`. Multi-line input is supported.
