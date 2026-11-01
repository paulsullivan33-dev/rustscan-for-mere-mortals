# The Moving Parts

You finish this chapter able to name
the five parts of a RustScan run —
targets, ports, batches, the timeout,
and the follow-up — and to guess which
part is responsible when a run behaves
strangely.

## The knock: ordinary connections

RustScan scans by *connecting*. For
each port it opens a normal TCP
connection, the way a browser would.
If the connection completes, something
is listening: the port is **open**. If
the machine refuses it, the port is
**closed**. If nothing comes back at
all before the **timeout**, RustScan
moves on and counts the port as not
open — which is a guess wearing a
uniform, and chapter 7 returns to it.

Because the knock is an ordinary
connection, RustScan needs no special
privilege and no raw packet access.
This is its great portability — and
its boundary. Nmap's famous SYN scan,
which knocks without completing the
connection, needs raw sockets and
administrator rights; RustScan simply
does not contain that machinery. What
it contains is speed.

## Batches and the file limit

Nobody knocks on 65535 doors one at a
time. RustScan knocks in **batches** —
by default, up to **4500 connections
in flight at once**. Every connection
in flight holds one **file descriptor**,
the operating system's unit for an open
connection, and every user has a limit
on those. The lab's shell allowed 4096:

```bash
ulimit -n
```

```text
4096
```

so the very first default run announced
the collision in plain language
(transcript t03):

```text
[!] File limit is lower than default batch size.
    Consider upping with --ulimit.
```

That warning is the moving part to
remember: **batch size is capped by
the file limit**, and the two flags
`-b` and `--ulimit` (chapters 7 and 13)
exist to negotiate between them. On a
real network the batch is also a
courtesy and a quality knob — a batch
too large for the target or the path
loses answers, and lost answers read
as closed doors.

## The timeout and the tries

Each connection waits at most
**1500 milliseconds** (the `-t` flag)
before being counted closed, and gets
**1 try** (the `--tries` flag) by
default. On loopback, where answers
arrive in well under a millisecond,
those numbers are nearly meaningless —
the lab proved that, too, in chapter 7.
On a real network they are the
difference between a scan that finds
the slow services and one that files
them as absent.

## Targets and ports are separate lists

`-a` says *which machines*: one
address, several, a CIDR range like
`192.168.1.0/24`, hostnames, or a file
of them (chapter 9). `-r` says a
*range of doors* (`1-1000`), `-p` a
*list* (`80,443,8080`), and `-e`
*exclusions* from either. Targets
times ports is the size of the job;
chapter 6 keeps those two lists from
being confused with each other, and
with `--top`.

## The follow-up: nmap as second stage

Unless you ask for the greppable
one-line output (`-g`, "greppable mode.
Only output the ports. No Nmap", as
the help puts it), RustScan finishes
by running **nmap** on just the open
ports. Everything after a `--` on the
command line is passed to nmap as its
own flags:

```bash
rustscan -a 127.0.0.1 -p 18083,18090,18091 -- -sT -sV
```

and the lab's transcript t05 shows the
exact command RustScan built from
that. The default follow-up, with no
flags of yours, asks nmap for a great
deal — more than a bare connect scan —
and on machines without raw-socket
privilege it fails. Chapter 8 is the
whole story.

## The config file

Settings you keep retyping can live in
a TOML **config file**, expected at
`~/.rustscan.toml` unless `-c` points
elsewhere (or `--no-config` skips it).
Flags on the command line override the
file. Chapter 9 runs the lab's sample
file, which reproduces a whole scan —
range, batch, greppable output — with
no scan flags on the command at all.

## Which part holds what

| Part | Holds | Set by |
| --- | --- | --- |
| Targets | which machines get knocked on | `-a` |
| Ports | which doors, as range or list | `-r`, `-p`, `-e` |
| Batch | how many knocks fly at once | `-b`, capped by the file limit |
| Timeout | how long a silent door is waited on | `-t`, `--tries` |
| Follow-up | what nmap asks the open doors | everything after `--` |
| Config | all of the above, kept in a file | `~/.rustscan.toml`, `-c` |
