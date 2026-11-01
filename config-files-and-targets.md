# Config Files and Target Lists

You finish this chapter able to run a
whole scan from a file — settings in a
config file, targets in a list —
which is the form a *standing* scan
takes: the weekly audit of chapter 10
is this chapter with a schedule.

## The config file

RustScan reads its settings from a
TOML file, expected at
`~/.rustscan.toml`, or wherever `-c`
points. `--no-config` makes it ignore
the file for one run. The lab kept its
sample in the repository
(`rustscan-lab/config-sample.toml`):

```toml
range = { start = 18080, end = 18100 }
greppable = true
batch_size = 500
timeout = 1500
tries = 1
scan_order = "Serial"
```

Pointed at that file, the scan needs
no scan flags at all (transcript t06):

```bash
rustscan -c rustscan-lab/config-sample.toml -a 127.0.0.1
```

```text
127.0.0.1 -> [18083,18084,18090,18091]
```

Greppable output, the range, the
smaller batch — all from the file.
Command-line flags override file
settings for that run, which is the
right arrangement: the file holds your
house standard, the command line
holds today's exception. Two cautions
worth the space. First, the file is
read *silently* — a scan behaving as
if you typed flags you didn't is
usually a config file you forgot;
`--no-config` settles the question.
Second, a config file in a home
directory travels with the account,
not the project — a scan run from a
different account is a different scan.

## Targets from a file

The `-a` option accepts more than
addresses typed out: given a path to
a text file, it reads the targets from
it, one per line. The lab's
`rustscan-lab/targets.txt` holds a
single line, `127.0.0.1`:

```bash
rustscan -a rustscan-lab/targets.txt -r 18080-18100 -g
```

```text
127.0.0.1 -> [18083,18090,18091]
```

(the neighbour had left by then —
results track the world, not the
script). A file is how a real target
list lives: the handful of machines
that are yours, named once, reviewed
occasionally, scanned as a set.
Addresses can also be CIDR ranges and
hostnames; hostnames are resolved
when the run starts, and chapter 13
records what an unresolvable name
does — in greppable mode it aborts
the run *silently*, exit 1, which is
one more reason standing scans should
be checked against a known listener
before their silence is trusted.

Exclusions work for addresses too:
`-x` removes targets from the set,
the address-level twin of chapter 6's
`-e` for ports.

## Scan order

`--scan-order` chooses the knocking
pattern: `serial` (the default) walks
the ports in ascending order;
`random` shuffles them (transcript
t06):

```text
127.0.0.1 -> [18091,18090,18084,18083]
```

The result set is the same; the order
of arrival is not. Serial order makes
runs easy to compare line by line.
Random order spreads the knocking
across the port space instead of
marching — which some operators
prefer for the target's sake, and
which makes two runs' raw output
differ even when nothing changed.
Note, though, that even serial runs
may print ports out of order (the
`-t 50` run in transcript t04 did):
within a batch, connections finish
when they finish. Order in the output
is presentation, never evidence.
