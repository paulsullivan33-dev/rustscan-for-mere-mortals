# What RustScan Is

You finish this chapter able to say
what a port scan is, why RustScan
exists when nmap already does the job,
and where the legal and polite boundary
of scanning sits — before any command
appears.

A **port** is a numbered door on a
machine. The machine has one network
address; the doors, numbered 0 to
65535, are how many different programs
share it. A web server might wait at
door 443, a file share at 445, a game
at some five-digit number nobody chose
on purpose. A program waiting at a door
is **listening**, and the door is
**open**. A door with nobody behind it
is **closed**: knock, and the machine
answers at once that nobody is home.

**Port scanning** is knocking —
systematically, quickly, and writing
down which doors open. On your own
machine it is an audit: this is what I
am offering the network, including the
test server I started in March and
never stopped. Done to a machine that
isn't yours, the same knock is
reconnaissance, which is why this
chapter states the rule before the
tool:

> **Scan only systems you own, or
> systems you have explicit permission
> to test.**

Not "systems you can reach." Not
"systems nobody would mind about."
Ownership, or permission you could
show someone. Laws differ by place —
unauthorised scanning is an offence in
some jurisdictions and a terms-of-service
violation nearly everywhere — and the
practical risk needs no law at all: a
fast scan looks exactly like the first
minute of an attack, and it is treated
that way by the people watching. Every
target in this guide is **loopback**,
the address `127.0.0.1` where a machine
talks to itself, or is named in the
text as the reader's own machine. The
skills transfer whole to your own
servers and your own network. They are
not demonstrated on anyone else's, and
they should not be practised on anyone
else's either.

## Why a second tool exists

The classic scanner is **nmap** (its
own guide in this series teaches it
properly). Nmap can do the knocking
itself, and on a short list of doors it
is quick. But nmap was built for depth
— services, versions, scripts, operating
systems — and a first pass over all
65535 doors is only the beginning of
its work. On a slow or distant target
that first pass can take long enough
that people simply don't run it, and
the audit doesn't happen.

**RustScan is the first pass, built as
its own tool.** It is a small program
written in Rust that does one thing —
knock, very fast, using ordinary TCP
connections, in large parallel
**batches** — and then does the wisest
thing a specialist can do: it hands
the doors that opened to nmap, with
your nmap flags attached, and gets out
of the way. RustScan finds; nmap
explains. Chapter 8 lives in that
hand-off.

The speed is real and the lab measured
a piece of it: all 65535 ports of
loopback, knocked and answered in
about six seconds (transcript t06b).
Hold the celebration, though — chapter
7 is honest about what loopback timings
cannot tell you, and chapter 5 shows
the strange artefacts that appear when
a machine knocks on *itself* this
fast.

## A first taste

After installing (chapter 3), a scan of
your own machine, over a small range,
in the quiet machine-readable form, is
one line:

```bash
rustscan -a 127.0.0.1 -r 18080-18100 -g
```

```text
127.0.0.1 -> [18083,18090,18091]
```

That is the whole shape of the tool:
an address, the doors that opened, in
one line a script can read. The lab's
line had a fourth door in it — a
neighbour's, on a shared machine —
and chapter 4 tells that story,
because "your scan found a service you
didn't start" is a normal Tuesday with
this tool, not an emergency.

## What it is not

RustScan is not nmap's replacement: it
identifies nothing, fingerprints
nothing, and its own answer is just a
list of numbers. It is not quiet: a
default batch opens thousands of
connections a second, every one of
them visible to anything watching, and
its own help text warns that sensitive
servers may not enjoy the attention —
another reason the permission rule is
about more than politeness. And it is
not evidence of anything by itself on
loopback, where its speed manufactures
ghosts (chapter 5). It is a fast first
pass with an honest second stage, used
on machines that are yours.
