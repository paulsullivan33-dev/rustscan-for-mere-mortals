# The Neighbours

You finish this chapter able to say
when RustScan is the right tool and
when one of its neighbours is —
honestly, including the large territory
where the neighbour wins. These tools
are characterised from their
documentation and from this guide's
own nmap runs; the neighbours were not
benchmarked in this lab, and nothing
here pretends they were.

## nmap, on its own

The neighbour RustScan lives with.
Nmap scans by itself perfectly well —
chapter 8's plain `nmap -sT` run did —
and everything past the first pass
belongs to it outright: service and
version detection, OS fingerprinting,
the script engine, UDP scanning,
careful timing for slow or defended
targets, and output formats built for
records. It also owns the SYN scan,
the half-open knock that needs raw
sockets and privilege.

So when is RustScan the tool? When
the question is *"which doors, out of
tens of thousands, are open on my
machines?"* and the answer is needed
fast enough that you'll actually ask
weekly. When the question starts with
*what*, *which version*, *is it
vulnerable*, *why is it silent* — the
question is nmap's, whether RustScan
ran first or not. The pipeline of
chapter 8 is not a compromise between
the two; it is each tool doing the
half it is for. The nmap guide in
this series is the natural next read.

## masscan

The other famous sprinter.
Masscan scans at internet scale —
millions of packets per second, whole
address ranges, with its own built-in
TCP stack doing the knocking. It is
built for researchers measuring the
entire internet, and it pays for that
speed with rawness: raw sockets and
privilege required, results that need
careful handling, and a blast radius
that makes RustScan's default batch
look like knocking politely. On a
home or workshop network it is the
wrong instrument — and on a machine
like this lab's, with no raw sockets
at all, it cannot even start. If your
scanning life is a rack of your own
servers, RustScan's connect scans are
the mortal-scale version of the same
idea.

## naabu

A closer cousin: a fast port scanner
from the ProjectDiscovery toolkit,
written in Go, designed to pipe its
findings into other tools in that
family (httpx for web probing, nuclei
for vulnerability checks). Naabu can
use connect scans like RustScan or
SYN scans with privilege, and its
strength is the pipeline around it —
if your work already lives in that
toolkit, naabu is the natural first
pass. RustScan's counter-claims are
its nmap hand-off (naabu's ecosystem
points elsewhere) and a single static
binary with a config file a mortal
can hold in their head. Two honest
tools for the same job; the seam you
need decides.

## ZMap

The research end of the family: a
single-packet scanner built to survey
the whole IPv4 internet for one port
in under an hour, from a properly
provisioned machine. It answers
questions like "how many machines on
Earth answer on 443?" — a census, not
an audit. Nothing in this guide's
world — your machines, your network,
your doors — needs it, and its
operating assumptions (bandwidth,
privilege, a network that tolerates
being a firehose) are the opposite of
a home lab's. It is named here so the
family portrait is complete, and so
its name is not mistaken for a bigger
version of this chapter's tool.

## The short version

One machine or a handful, doors
audited regularly, details wanted on
what you find: RustScan into nmap.
Deep questions about one target: nmap
alone, from the start. A pipeline of
security tools already in place:
naabu fits it. The whole internet:
masscan and ZMap, which are research
instruments with research-sized
consequences, and not this series'
idea of a Saturday tool.
