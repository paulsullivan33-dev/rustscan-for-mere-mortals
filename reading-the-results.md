# Reading the Results

You finish this chapter able to read
any RustScan run — a list, a short
list, or silence — and to cross-examine
a surprising result before believing
it. That second skill matters more,
because at RustScan's speed, on
loopback, some of what it reports is
not there.

## The three shapes of an answer

A greppable run ends in one of three
shapes, all demonstrated in chapter 4:

- **A list** — `127.0.0.1 -> [18083,18090,18091]`.
  These ports accepted a connection.
- **A shorter list than you expected** —
  some of your doors are missing. The
  service may have stopped, may listen
  somewhere else (a different address),
  or the run's timeout gave up on it.
- **Silence, exit 0** — nothing in the
  range accepted a connection. That is
  an answer, not an error: transcript
  t08 is chapter 4's exact scan re-run
  after the fixture servers stopped,
  and the correct output was nothing.

Notice what never appears in greppable
mode: the words *closed* or *filtered*.
RustScan reports presences. A port
that refused, and a port whose answer
never came back, are both simply
absent. The distinction between
*refused* (a machine actively saying
no) and *silent* (a firewall eating
the question, or a service too slow
for the timeout) is real, it matters,
and it belongs to the nmap stage —
chapter 8's `-sT` run at least prints
states for the ports you name, and the
nmap guide goes the rest of the way.

## Open means "accepted a connection"

RustScan's whole test is: did a TCP
connection complete? That is a strong,
simple fact — and only that fact. It
does not say *what* accepted. The lab
knew its three ports were Python web
servers because it had started them;
the identification of the neighbour's
port 18084 as a web server came from
asking it (curl showed its server
banner), and the identification of the
fixture ports in chapter 8 came from
nmap's service detection. A number in
the list is a claim of *presence*,
never of identity. Treat every result
as "something was listening here, at
that moment" and you will read scans
correctly for the rest of the book.

## Ghost ports: the loopback artefact

Now the strange part, which the lab
met the first time it scanned the
whole port space (transcript t06b):

```text
127.0.0.1 -> [18083,18090,18091,40784,49094,49248,49618,55432]
```

Some of those are genuine neighbours
(55432 was another tenant's database).
But 40784, 49094, 49248 and 49618 had
no listener at all — and the *next*
full scan named a different set of
strangers (34072, 49894, 58178), and a
later one another (45894, then 53764).
A service does not move house between
scans. These are **ghost ports**.

The mechanism is a known loopback
curiosity. When any program on the
machine makes an outgoing connection,
the system assigns it a temporary
**ephemeral port** as its return
address. A fast scan of loopback is
thousands of outgoing connections,
each grabbing an ephemeral port, each
aimed at 127.0.0.1. Now and then the
ephemeral port a connection is given
*is* the port it was sent to knock on —
and the machine, asked to connect to
itself at its own return address,
completes a connection to itself. The
port reports open. Nothing was ever
listening there; by the time you
look, the socket is gone.

Three tells, all in the transcripts:
the suspect ports are high (ephemeral
ports live up in the tens of
thousands); the set changes every run;
and nothing else can find them. The
lab cross-examined one properly
(transcript t06b):

```bash
ss -tln | grep 53764        # no listener
curl -s http://127.0.0.1:53764/   # exit 7: connection refused
```

## The checking habit

So the method of this chapter, worth
more than any flag: **verify every
surprise with a second, slower tool
before you act on it.**

- `ss -tln` — the machine's own list of
  listeners. A real service is here.
- A direct request — curl for a web
  port, or the service's own client.
- The lab's `verify-ports.py`
  (transcript t09), which takes a
  greppable result line and re-checks
  each port with one plain connection
  at a time:

```bash
python3 rustscan-lab/verify-ports.py "127.0.0.1 -> [18083,18084,53764]"
```

```text
127.0.0.1:18083 OPEN
127.0.0.1:18084 REFUSED (ConnectionRefusedError)
127.0.0.1:53764 REFUSED (ConnectionRefusedError)
```

Ghosts are mostly a loopback disease —
they need the scanner and the target
to share one machine's port pool — but
the habit is universal: a scan is a
witness, and witnesses get
cross-examined, especially fast ones.
