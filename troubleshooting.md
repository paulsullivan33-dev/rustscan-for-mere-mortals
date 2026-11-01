# Troubleshooting

You finish this chapter able to name
the cause of each failure the lab
actually met — every one below is in
the transcripts — and the one check
that settles each. They are ordered
roughly by how early a new user meets
them.

## "File limit is lower than default batch size"

**Cause.** Your file-descriptor
ceiling (`ulimit -n`) is below the
batch size (default 4500), as the
lab's 4096 was (transcript t03). The
scan still runs; RustScan has told you
the batch cannot all fly at once.

**Settle it.** Either lower the batch
(`-b 500`) or, as a deliberate
machine-level choice, ask for a higher
limit (`--ulimit 60000`) — chapter 7
weighs both. What not to do is ignore
it and then trust a *silence*: a batch
starved of descriptors can lose
answers. (The `--ulimit` run is
transcript t04.)

## The follow-up fails: "Error Exit code = 1"

**Cause.** The scan succeeded; the
default nmap hand-off died. On
machines without raw-socket privilege
the default follow-up's aggressive
requests cannot open a raw socket —
proven directly in transcript t05 by
running `nmap -A` by hand and getting
`Couldn't open a raw socket`. A
missing nmap lands in the same place.

**Settle it.** Hand it connect-scan
flags: `-- -sT -sV` (chapter 8).
Confirm nmap exists with
`nmap --version`. Your `Open` lines
were real; only the explanation stage
failed.

## A range scan prints nothing at all

Four different causes wear this one
face. Work them in this order
(transcript t07 for all four):

1. **Nothing is open.** Check with
   `ss -tln`: if the machine agrees,
   the silence is the truth (t08).
2. **The range is backwards.**
   `-r 18100-18080` exits 0, prints
   nothing, complains never. Read your
   own command.
3. **The batch size is zero.** `-b 0`
   also exits 0 and silently scans
   nothing — even over open ports.
4. **The name did not resolve.** In
   greppable mode an unresolvable
   target prints nothing and exits 1;
   without `-g` it says so:
   `Host "no-such-host.invalid" could
   not be resolved.` Check the exit
   code, and re-run without `-g` when
   a silent run matters.

## The scan found a port that does not exist

**Cause.** A ghost: chapter 5's
loopback self-connection. The port is
high, it was not in `ss`, and the next
scan names different strangers.

**Settle it.** The chapter 5
cross-examination: `ss -tln`, a direct
request, `verify-ports.py`, a re-scan.
Four witnesses, and the ghost fails
all of them. Do not write firewall
rules, tickets or alarmed messages
about a port only one fast scan has
seen.

## The scan found a port you didn't start

**Cause.** Somebody did start it —
another user of the machine, another
service of yours, another tenant
(transcript t02's port 18084, gone by
transcript t06b). Scans report the
machine, not your intentions.

**Settle it.** Identify it before
judging it: `ss -tlnp` shows the owning
process where you have the privilege,
and chapter 8's hand-off names the
service. On a machine that is wholly
yours, an unnameable listener is the
audit earning its keep; on a shared
one it is usually a neighbour, and
`-e` (chapter 6) keeps it out of your
standing results.

## "invalid value '99999' ... is not in 0..=65535"

**Cause.** A port list entry outside
0–65535 (transcript t07), caught by
the parser before anything ran, exit
2. The friendliest failure in the
tool: it tells you the flag, the
value and the rule.

## Results change between identical runs

**Cause.** Usually the world, not the
tool: a service stopped, a neighbour
left, ghosts rotated. Port *order*
inside the brackets also varies
freely — batches finish in the order
connections complete (transcript
t04's unsorted line).

**Settle it.** Compare sets, not
strings; expect the high-port tail of
a loopback scan to churn; and let
`ss` arbitrate any difference that
matters.
