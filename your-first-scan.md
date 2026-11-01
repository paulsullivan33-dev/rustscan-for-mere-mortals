# Your First Scan

You finish this chapter having scanned
your own machine and found exactly the
doors you opened for the purpose — the
one exercise every later chapter
refers back to. The lab did it with
three toy web servers; you will do it
with one.

## Set up a door you control

A scan with nothing to find teaches
nothing, so first, be a service. Any
small web server will do; Python's is
on most machines already. This serves
the current folder on port **18083** of
loopback, and only loopback:

```bash
python3 -m http.server 18083 --bind 127.0.0.1
```

Leave it running. The lab started
three of these — on 18083, 18090 and
18091, each serving a different fixture
page ("fixture alpha", "fixture
bravo", "fixture charlie") — so its
results would be unmistakable.
Transcript t01 shows them listening:

```text
LISTEN 0  0  127.0.0.1:18091  0.0.0.0:*
LISTEN 0  0  127.0.0.1:18090  0.0.0.0:*
LISTEN 0  0  127.0.0.1:18083  0.0.0.0:*
```

and answering a browser's question
(curl) with their pages. That `ss`
listing is your pre-scan truth: the
machine's own account of what is
listening, against which the scan's
account can be checked. Keep that
habit — chapter 5 makes a method of
it.

## The scan

Scan a small range around your port,
in greppable mode (`-g`), which prints
the one-line result and skips the
nmap follow-up for now:

```bash
rustscan -a 127.0.0.1 -r 18080-18100 -g
```

The lab's result (transcript t02):

```text
127.0.0.1 -> [18083,18084,18090,18091]
```

Three of those are the fixtures —
18083, 18090, 18091, found correctly.
The fourth, **18084**, nobody in the
lab had started. The lab machine is
shared, and another tenant's web
server was listening there that
evening; by the next scan it had gone
(transcript t06b checks, and t08's
machine has one fewer tenant still).
The scan was not wrong. A scan reports
*everything listening*, not just the
things you meant to start — on a
shared machine, a family computer, or
a server with other administrators,
"a door I didn't open" is information,
not an error. It is also the practical
core of chapter 1's rule: the same
knock that finds your forgotten test
server finds other people's services
just as happily, which is why it is
only run where you have the right.

Your single-server version of this
scan should print your one port. If it
prints more, you have met the same
lesson early: check each extra with
`ss -tln` before you believe the
machine has a mystery.

## Two smaller scans

Name the doors exactly, and the answer
shrinks to them:

```bash
rustscan -a 127.0.0.1 -p 18083,18090,18091 -g
```

```text
127.0.0.1 -> [18083,18090,18091]
```

And scan a stretch where nothing
listens, to learn what *nothing* looks
like in this tool:

```bash
rustscan -a 127.0.0.1 -r 18085-18089 -g
```

```text
(exit 0, and no output at all)
```

Silence, exit code 0, is a successful
scan that found nothing. Greppable
mode has no "all closed" line to print.
Chapter 5 builds the reading of
results on these three shapes: a list,
a smaller list, and silence.

## Without the -g

Run the first scan once more with no
`-g` and you get the full ceremony:
the banner (there is a `--no-banner`
flag, and scripts will want it), the
config-file note, the file-limit
warning from chapter 2, an `Open` line
per door — and then the nmap
follow-up, which on the lab machine
failed with `Error Exit code = 1`
(transcript t03). That failure is not
your scan failing; the doors were
found and printed before it happened.
It is the subject of chapter 8, and
the fix is a pair of flags of your
own.
