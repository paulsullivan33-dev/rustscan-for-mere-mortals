# Glossary

**Address (target)** — a machine to
scan: an IP address, a hostname, a
CIDR range, or a file of them, given
with `-a`.

**Batch size** — how many connections
RustScan keeps in flight at once
(`-b`, default 4500). The throttle of
the scan, capped by the file limit.

**CIDR range** — a block of addresses
written as a network and a size, such
as `192.168.1.0/24`: the 256 addresses
of a typical home network.

**Closed port** — a port where the
machine answers the knock by refusing
the connection: a definite "nobody
listens here".

**Config file** — the TOML file
(`~/.rustscan.toml`, or the path given
to `-c`) holding scan settings so
they need not be typed each run.

**Connect scan** — scanning by
completing ordinary TCP connections
(nmap's `-sT`; the only kind RustScan
itself performs). Needs no special
privilege.

**Ephemeral port** — a temporary
high-numbered port the system assigns
as the return address of an outgoing
connection. The raw material of ghost
ports.

**File descriptor (fd) limit** — the
operating system's ceiling on how many
connections and files a process may
hold open at once, shown by
`ulimit -n`. Every in-flight knock
spends one.

**Filtered port** — a port whose
knocks get no answer at all, usually
because a firewall discarded them.
RustScan reports it only as absence;
nmap makes the distinction.

**Ghost port** — a port a loopback
scan reports open that no service
listens on: the scanner's own
connection completed to itself through
an ephemeral port. Proven, and named,
in chapter 5.

**Greppable mode** — the `-g` flag:
output as one machine-readable line
per host (`127.0.0.1 -> [18083,18090]`)
and no nmap follow-up.

**Hand-off** — RustScan's second
stage: the open ports passed to nmap,
with the user's flags from after
`--`, for service identification and
everything deeper.

**Listening** — a program waiting for
connections on a port. `ss -tln`
lists a machine's listeners.

**Loopback** — the address range
(127.0.0.1 above all) on which a
machine talks to itself. This guide's
only demonstrated target.

**Open port** — a port where a
connection completed: something was
listening at that moment. A claim of
presence, never of identity.

**Port** — a numbered door, 0–65535,
by which programs share one machine's
network address.

**Range** — a span of ports written
`start-end` for `-r`, scanned
inclusively — and, written backwards,
scanned as nothing, silently.

**Raw socket** — direct access to
packets below the connection level.
SYN scans and OS fingerprinting need
it; connect scans do not; this lab's
machine forbade it entirely.

**Service detection** — nmap's `-sV`:
speaking to an open port to name the
program listening, from its banner
and behaviour.

**SYN scan** — nmap's half-open scan:
the knock is a single SYN packet and
the connection never completes. Fast
and quiet, and it needs raw sockets.

**Timeout** — how long one connection
attempt waits for an answer before
the port is counted closed (`-t`,
milliseconds, default 1500).

**Top ports** — a shortlist of the
most commonly used ports, offered by
the `--top` flag — which in this
guide's tested build did not limit
the scan as its help promises
(chapter 6).

**Tries** — how many attempts a silent
port receives before being counted
closed (`--tries`, default 1).
