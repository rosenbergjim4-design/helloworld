# helloworld

A tiny task list, used as a sandbox for [dsh-superagent](https://github.com/deepseek-ai/dsh-superagent-prototype).

```sh
python3 src/cli.py add "write the README" -t docs
python3 src/cli.py ls
python3 src/cli.py done 1
python3 src/cli.py stats
```

Tasks are stored as JSON in `~/.todo.json`, or wherever `--file` points.

## Tests

```sh
python3 -m pytest tests/ -v
```

Two tests currently fail on purpose — they cover the first two entries in
[ISSUES.md](ISSUES.md).

## Known issues

See [ISSUES.md](ISSUES.md).
