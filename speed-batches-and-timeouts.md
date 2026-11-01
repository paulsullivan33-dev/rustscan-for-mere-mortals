# Speed — Batches, Timeouts and Limits

You finish this chapter knowing the
three numbers that govern how fast a
scan goes and how much it can be
trusted — batch size, the file limit
behind it, and the timeout — and which
of them loopback can teach you about
and which it cannot.

## The batch is the throttle

RustScan's speed comes from doing
thousands of connections at once. The
`-b` flag sets how many: the **batch
size**, 4500 by default. Batches are
also the load you place on everything
involved — your own machine, the
network path, and above all the
target, whose doorway you are
crowding. The tool's own help carries
the warning: a big batch pointed at a
sensitive server is a small flood.

## The file limit is the ceiling

Every connection in flight spends one
**file descriptor**, and your account
has a ceiling (`ulimit -n`). The lab's
ceiling was 4096, *below* the default
batch — hence the warning in
transcript t03. Two honest responses:

- **Lower the batch to fit** — `-b 500`
  is a perfectly respectable scan, and
  on most real networks the polite and
  the accurate choice besides.
- **Raise the ceiling with `--ulimit`** —
  `rustscan --ulimit 60000` asks
  RustScan to raise the limit for its
  own process. Whether the system
  grants it depends on your hard limit
  and your privileges; on the lab
  machine (running as root) the run
  in transcript t04 accepted the
  request without complaint. Raising
  limits is a machine-level decision,
  not a per-scan habit: a ceiling
  exists partly so one enthusiastic
  program cannot spend the whole
  machine's connections.

## What the lab measured

Ten thousand loopback ports, three
batch sizes (transcript t04):

```text
-b 4500 (default)   0.80 s
-b 500              0.67 s
-b 100              0.62 s
```

Read that table the way chapter 5
would: on loopback, batch size barely
mattered, and the differences are
within the noise of a shared machine.
That is not a discovery that small
batches are faster. It is a discovery
that **loopback cannot measure this**:
the answers are instant, the
connections are free, nothing is
crowded, so the throttle has nothing
to throttle. On a real network — a
target across WiFi, a server with a
busy doorway — batch size is the
difference between a scan that hears
every answer and one that tramples
half of them. The lab reports its
numbers and declines to extrapolate;
your network's numbers are yours to
measure, starting low.

## The timeout and the tries

`-t` sets how long, in milliseconds,
a connection waits before the port is
counted closed (default 1500).
`--tries` sets how many attempts a
silent port gets (default 1). Together
they are the scan's *patience*, and
patience is accuracy: a slow service
given 100 ms looks exactly like a
closed door.

The lab starved the timeout to prove
the point about loopback (transcript
t04): at `-t 50`, and even at `-t 1` —
one millisecond, three runs in a row —
every fixture was still found, because
loopback answers in a fraction of a
millisecond. Do not let that reassure
you about real targets. On a network,
choosing a timeout is choosing which
slow truths you will miss; the
defaults (1500 ms, 1 try) are sane,
and the honest way to scan something
you care about is to raise the tries
before you raise the speed.

## The standing advice

Start with the defaults. Lower the
batch when the target is small,
distant, shared or sensitive — which
is most targets worth scanning. Treat
the file-limit warning as information
about your machine, not an obstacle
to defeat. And remember what chapter
1 said about the audience of a fast
scan: at full batch, your knocking is
the loudest thing on the network, and
every watcher knows whose it is.
