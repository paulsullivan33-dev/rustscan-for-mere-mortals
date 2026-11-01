# RustScan for Mere Mortals

Every program that listens on a network
waits at a numbered door — a **port**.
A file server, a web page, a game, a
printer: each sits behind its own door
on its machine, and the machine's
address plus the door's number is how
anything reaches it. Knowing which
doors are open on your own machines is
basic housekeeping: it tells you what
you are offering the network, including
the things you forgot you were offering.

Asking about doors has a classic tool —
**nmap**, the subject of its own guide
in this series — and nmap is thorough.
It is also, on a first pass over
thousands of doors, patient. **RustScan**
is the sprinter that runs ahead of it.
It knocks on every door at extraordinary
speed using ordinary connections, writes
down which ones opened, and then —
this is the part people miss — it hands
that short list to nmap to do the
careful work. RustScan finds; nmap
explains. This guide teaches both
halves, and it teaches them on the one
target nobody needs permission for:
your own machine, talking to itself.

**The ethics line, before anything
else, because this tool needs it in
front:** scanning a machine you do not
own, or have not been explicitly asked
to test, ranges from rude to illegal
depending on where you live and whose
machine it is. Every scan in this guide
targets **loopback** — the machine
scanning itself — or machines the
text names as yours. Keep yours the
same way. Chapter 1 returns to this
before the first command appears.

The lab behind this guide ran the real
thing: **RustScan 2.4.1**, the official
release binary, against three small
web servers it started itself on
loopback ports, with **nmap 7.94**
waiting for the hand-off. It scanned
ranges big and small, timed batches,
starved the timeout down to a single
millisecond, and read the results with
suspicion — which the results deserved.
Loopback scanning at this speed turns
up **ghost ports**: doors that were
never services, conjured by the scan's
own connections colliding with
themselves. The lab caught them,
proved them ghosts with a second tool,
and chapter 5 teaches you the same
check. It also caught this build's
`--top` flag behaving nothing like its
help text, and said so rather than
copying the help into the chapter.

What the lab could not do, it did not
fake. Its world has no raw sockets, so
nmap's SYN scans and the default
aggressive hand-off fail there — the
guide shows the failure, names the
cause, and teaches the connection-scan
path that works without privilege. Its
world also has no network beyond
loopback and no UDP, so LAN timing and
UDP scanning are taught from the
documentation and labelled as such.
Loopback answers in milliseconds;
nothing here claims your network will.
`criteria.md` keeps the full ledger.

## What this guide covers

- [**What RustScan is**](what-rustscan-is.md) —
  the two-stage idea: a very fast knock
  on every door, then nmap for the
  details — and the permission rule
  that governs all of it
- [**The moving parts**](the-moving-parts.md) —
  the scanner engine, batches and the
  file-descriptor limit that caps them,
  the timeout, the config file, and
  nmap waiting at the end
- [**Installing RustScan**](installing-rustscan.md) —
  the official release, the package and
  binary routes, and the version check
  that proves it runs
- [**Your first scan**](your-first-scan.md) —
  three small servers started on
  purpose, one range scanned, and the
  extra open door nobody expected
- [**Reading the results**](reading-the-results.md) —
  open, closed and silent; the greppable
  line; and the ghost ports — how to
  check a surprise before believing it
- [**Ranges, lists and the top ports**](ranges-lists-and-top.md) —
  `-r`, `-p`, exclusions, and an honest
  account of what `--top` did in the lab
- [**Speed — batches, timeouts and limits**](speed-batches-and-timeouts.md) —
  the batch size against the file
  limit, what the timeout can and
  cannot teach you on loopback, measured
- [**The nmap hand-off**](the-nmap-handoff.md) —
  passing your own flags after `--`,
  service detection with `-sT -sV`, and
  why the default hand-off needs more
  privilege than a connect scan does
- [**Config files and target lists**](config-files-and-targets.md) —
  the same scan with no flags at all,
  addresses read from a file, and scan
  order
- [**Recipes**](recipes.md) — audit your
  own machine's whole port space, keep
  a weekly greppable record, hand one
  service to nmap for a close look, and
  verify every surprise
- [**The neighbours**](the-neighbours.md) —
  nmap on its own, masscan, naabu and
  ZMap: what each does that RustScan
  doesn't, and vice versa
- [**Limits**](limits.md) — connect
  scans only, ghosts on loopback, a
  `--top` flag that misbehaves in this
  build, silent failures in greppable
  mode, and speed that can be its own
  problem
- [**Troubleshooting**](troubleshooting.md) —
  the file-limit warning, the hand-off
  that exits 1, the batch size that
  silently scans nothing, and the scan
  that finds doors which do not exist
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Scanning other people's systems — not
as technique and not as target practice;
the permission rule in chapter 1 is the
whole position. Evading firewalls or
intrusion detection: this is a
housekeeping tool used in the open, on
your own doors. The deep nmap craft —
scripting, OS fingerprinting, timing
templates — belongs to the nmap guide;
here nmap is the second stage of
RustScan's pipeline, taught to the
depth the hand-off needs.

## How to use this guide

Read chapter 1 for the model and the
rule, and chapter 2 before installing —
knowing which part holds what turns
later surprises (a warning about file
limits, a follow-up scan that fails)
into named problems. Chapter 4's scan
is the one to reproduce first: it is
small, it is your own machine talking
to itself, and everything later refers
back to it. Chapter 5 is the one to
read slowly: its habit — *check a
surprise before you believe it* — is
worth more than any flag in the book.
The lab's transcripts live in
`rustscan-lab/transcripts/`; its
fixture pages are `rustscan-lab/fixtures/`,
its config example is
`rustscan-lab/config-sample.toml`, and
its checking script is
`rustscan-lab/verify-ports.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [Nmap for Mere Mortals](https://paulsullivan33-dev.github.io/nmap-for-mere-mortals/)
- [Networking for Mere Mortals](https://paulsullivan33-dev.github.io/networking-for-mere-mortals/)
- [tcpdump for Mere Mortals](https://paulsullivan33-dev.github.io/tcpdump-for-mere-mortals/)
- [Netcat for Mere Mortals](https://paulsullivan33-dev.github.io/netcat-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/rustscan-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/rustscan-for-mere-mortals/blob/main/LICENSE-CODE).
