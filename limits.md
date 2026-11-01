# Limits

You finish this chapter able to recite
what RustScan cannot do — in the tool
itself, in this build of it, and in
the lab that tested it — so none of
them can surprise you mid-audit.

**Connect scans only.** RustScan
knocks by completing ordinary TCP
connections. It has no SYN scan, no
raw-packet craft, no OS fingerprint —
by design, and permanently. Anything
that needs those is nmap's job, after
the hand-off or instead of it.

**Presence, never identity.**
RustScan's entire finding is "a
connection completed here." What the
service is, whether it is the service
the port number suggests, whether it
is healthy — none of that is in the
tool. A scan result is the beginning
of an audit, not the audit.

**Ghost ports on loopback.** Scanning
your own machine at speed manufactures
open ports that are not services —
the self-connection artefact of
chapter 5, with a different cast every
run. On real networks the effect
mostly vanishes; on loopback, the
most common first target, it is
guaranteed eventually. Verification
is not optional garnish; it is part
of reading this tool's output.

**`--top` misbehaves in this build.**
Version 2.4.1's `--top`, run on its
own in the lab, scanned the whole
space instead of the help text's
thousand ports (chapter 6, transcripts
t06/t06b). Whether the fault is the
flag's or the interaction's, the
practical limit stands: only `-r` and
`-p` mean exactly what they say.
Verify choice-delegating flags on a
target you control before trusting
them anywhere else.

**Silence is overloaded.** In
greppable mode, "nothing open", "the
range was written backwards", "the
batch size was zero", and "the
hostname could not be resolved" can
all present as little or no output —
exit codes differ (0, 0, 0, and 1 in
the lab's tests) but a script that
only reads standard output cannot
tell them apart. Chapter 13 names each
one. A scan you act on deserves its
exit code checked and, for standing
scans, a known listener in range as a
heartbeat.

**Speed is a side effect.** The
default batch is 4500 simultaneous
connections, aimed at whatever you
name. On old, small, embedded or
fragile targets — the printer, the
router, the decade-old NAS — that is
not an audit, it is an incident.
RustScan's own help warns that the
target "may not be able to handle this
many socket connections at once". The
batch flag exists; use it downward
first.

**Loopback teaches loopback.** Every
number in this guide's lab is a
loopback number: milliseconds,
instant refusals, free connections.
Nothing measured here predicts a LAN
scan's timing, a WiFi target's
behaviour under batch load, or a
firewall's opinion of you. UDP
scanning exists in the tool (the
`--udp` flag) and is entirely outside
this lab's evidence — the sandbox has
no UDP at all — so the guide does not
teach it beyond naming it.

**IPv6 and exotica, untested.** The
hand-off line shows an `{{ipversion}}`
slot, and RustScan addresses IPv6
targets, but this lab scanned IPv4
loopback only. Claims stop where the
transcripts stop.
