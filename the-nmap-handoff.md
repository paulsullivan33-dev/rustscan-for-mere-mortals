# The Nmap Hand-off

You finish this chapter able to make
the second stage work anywhere: to
pass nmap the flags it needs, read
its service identifications, and
understand why the *default* follow-up
fails on machines without raw-socket
privilege — including, likely, yours
until you adjust it.

## How the hand-off works

When a non-greppable scan finds open
ports, RustScan builds an nmap command
from them: your flags after `--`, the
found ports, the target. Run with
flags of your own, it shows its work
(transcript t05):

```text
[>] Running script "nmap -vvv -p {{port}} -{{ipversion}} {{ip}} -sT -sV"
    on ip 127.0.0.1
```

Everything after the `--` is yours.
Everything else — the port list, the
address — RustScan fills in. This is
the entire design of chapter 2 made
visible: RustScan finds, nmap
explains, and the seam between them is
one command line you control.

## The working recipe: -sT -sV

Two nmap flags carry most of the
value:

- **`-sT`** — the *connect scan*: nmap
  asks with ordinary connections, the
  same unprivileged knock RustScan
  used. It needs no raw sockets.
- **`-sV`** — *service detection*: nmap
  speaks to each open port and reads
  its banner and behaviour to name
  what is listening.

```bash
rustscan -a 127.0.0.1 -p 18083,18090,18091 -- -sT -sV
```

The lab's result (transcript t05):

```text
PORT      STATE SERVICE REASON  VERSION
18083/tcp open  http    syn-ack SimpleHTTPServer 0.6 (Python 3.12.3)
18090/tcp open  http    syn-ack SimpleHTTPServer 0.6 (Python 3.12.3)
18091/tcp open  http    syn-ack SimpleHTTPServer 0.6 (Python 3.12.3)
```

All three doors identified as the
Python servers they were — the
identification RustScan itself never
attempts. One honest wrinkle in that
output: nmap labels the reason
`syn-ack` even for a connect scan on
loopback; the word is nmap's bookkeeping,
not a claim that raw packets flew.
Service detection also took **six
seconds** against RustScan's
milliseconds for the same ports — the
pipeline's proportions in one number:
finding is cheap, explaining is work.

For contrast, plain nmap on its own
(transcript t05) shows what the stages
look like unbundled:

```bash
nmap -sT -p 18083,18090,18091 127.0.0.1
```

```text
PORT      STATE SERVICE
18083/tcp open  unknown
18090/tcp open  unknown
18091/tcp open  unknown
```

Same doors, no names: that difference
is exactly what `-sV` buys.

## Why the default hand-off fails here

Run RustScan with no `--` flags and
the follow-up asks nmap for much more
than a connect scan — the aggressive
bundle, whose centrepiece (OS
detection and SYN-style probing) works
with **raw sockets**. The lab machine
forbids raw sockets outright, and the
default run died at the seam
(transcript t03):

```text
[~] Starting Script(s)
[!] Error Exit code = 1
```

The diagnosis is one direct experiment
away (transcript t05) — ask nmap for
the aggressive scan by hand:

```bash
nmap -A -p 18083,18090 127.0.0.1
```

```text
Couldn't open a raw socket. Error: Operation not permitted (1)
```

Note what did *not* fail in the
default run: the scan itself. The
`Open` lines printed before the error
are real results. The failure is
confined to the follow-up — which is
why the fix is not to fix RustScan but
to hand it humbler flags: `-- -sT`,
and `-sV` when you want names.

On your own machine, running nmap as
administrator (or with the raw-socket
capability granted) makes the default
bundle available — the nmap guide
covers that terrain. This guide's
position is that the connect-scan
hand-off is the one every reader can
run everywhere, so it is the one
taught as the default habit.

## Script levels

RustScan's `--scripts` flag chooses
how much nmap scripting follows the
scan: `none`, `default`, or `custom`.
The lab used the default level with
explicit flags. The deeper nmap craft
— its script engine, fingerprinting,
timing templates — is another guide's
subject and a large one; what this
chapter needs you to keep is the seam:
ports flow left to right, flags flow
in after `--`, and when the seam
breaks, the error belongs to whichever
side of it you are standing on.
