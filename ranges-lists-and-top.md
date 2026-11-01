# Ranges, Lists and the Top Ports

You finish this chapter able to say
exactly which doors a scan will knock
on — with a range, with a list, with
exclusions — and knowing one flag in
this build that does not do what its
help text says, because the lab
timed it.

## Ranges: -r

`-r 18080-18100` knocks on every port
from the first number to the last,
including both ends. A range is the
right shape when you are auditing a
neighbourhood: a block where you run
test services, the high ports a
workshop machine accumulates, or —
chapter 10's recipe — the entire
space, `-r 1-65535`.

One trap, found in transcript t07: a
range written backwards,

```bash
rustscan -a 127.0.0.1 -r 18100-18080 -g
```

exits 0 and prints nothing. It does
not complain that the range is empty;
it scans the emptiness faithfully and
reports it. If a range scan is
suspiciously silent, check the order
of the numbers before you check the
machine.

## Lists: -p

`-p 18083,18090,18091` knocks on
exactly those doors, no others. A list
is the right shape when you know what
you are looking for: the doors of one
application, the standard services a
machine *should* be offering, the
suspects from an earlier scan being
re-checked. List entries are checked
before the run — transcript t07 again:

```text
error: invalid value '99999' for '--ports <PORTS>':
  99999 is not in 0..=65535
```

(exit 2, and the clearest error this
tool produces). Ports run 0 to 65535;
the list parser enforces it, the range
parser, as seen above, is more
forgiving of nonsense.

## Exclusions: -e

`-e 18084` removes doors from whatever
the range or list selected. The lab
used it to remove the neighbour's
server from a range scan (transcript
t06):

```bash
rustscan -a 127.0.0.1 -r 18080-18100 -e 18084 -g
```

```text
127.0.0.1 -> [18083,18090,18091]
```

Exclusions are how a standing scan
stays honest on a machine you share:
the doors you have identified as
someone else's responsibility stop
decorating your results.

## The top ports: --top, honestly

The help text for `--top` says "Use
the top 1000 ports" — scan only the
doors services most commonly use,
nmap's style of shortlist. The lab
ran it (transcript t06, corrected by
t06b) and the results refused to fit
that story:

```text
127.0.0.1 -> [18084,18083,18090,18091,54338,55432]
```

Ports 18083, 18090 and 18091 are in no
top-1000 list on Earth; they are
five-digit fixture ports. And the
timing matched the wrong hypothesis.
From transcript t06b:

```text
-r 1-1000        0.13 s
--top            5.5 s
-r 1-65535       6.0 s
```

In this build, **2.4.1**, run as the
lab ran it, `--top` on its own behaved
like a scan of the whole space, not of
a thousand-port shortlist. (Paired
with an explicit range it respected
the range: `-r 18080-18100 --top`
returned exactly the fixtures.) The
guide reports this rather than
smoothing it over, because the
workaround is simple and the lesson
is general: **use `-r` and `-p` to say
what you mean, and treat any flag
that promises to choose for you as a
claim to verify once on a target you
control.** Chapter 4's fixtures are
exactly the place to verify it.

## Which to reach for

Auditing a block of your own services:
a range. Re-checking known doors: a
list. A standing scan on a shared
machine: either, plus exclusions. A
first look at an unfamiliar machine of
yours: a full range at a civilised
batch (chapter 7), then lists for the
follow-ups — and the previous section
is why "just use `--top`" is not this
guide's advice for that job.
