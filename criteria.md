# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The lab's fixtures are three invented web pages on loopback.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 12 names what the tool
   cannot do: connect scans only, presence never identity,
   ghost ports on loopback, a `--top` flag that in the tested
   build did not limit the scan as its help promises, silence
   that means several different failures, speed that is itself
   a hazard to fragile targets, and loopback numbers that say
   nothing about a real network.
8. **The ethics rule is in the text, early.** Scanning has one:
   scan only systems you own, or systems you have explicit
   permission to test. It is stated in the README and again in
   chapter 1, before the first scan command appears, and every
   target scanned anywhere in the guide and its lab is loopback
   — the author's own machine talking to itself. Nothing here
   is demonstrated on, or aimed at, anyone else's system.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a 2-CPU, 7.7 GB Ubuntu 24.04 sandbox,
shared with other tenants while the lab ran — other tenants'
listeners appear in the transcripts (an nginx on port 18084 and
a database on 55432) and are identified as theirs wherever they
appear; timings on a shared machine are reported as the ranges
they are. RustScan **2.4.1** (the current official release,
published 2025-02-23 by the project's current home,
bee-san/RustScan) was installed from the official release
archive `x86_64-linux-rustscan.tar.gz.zip` and run unmodified.
Nmap **7.94** was already present on the machine. The lab's
file-descriptor limit was 4096, soft and hard. All transcripts
live in `rustscan-lab/transcripts/`; the fixture pages are in
`rustscan-lab/fixtures/`, the config example is
`rustscan-lab/config-sample.toml`, the target list is
`rustscan-lab/targets.txt`, and the checking script is
`rustscan-lab/verify-ports.py`.

Every scan run in the lab targeted **127.0.0.1 only**. No other
address was scanned, at any point, for any test.

Run for real, with transcripts as evidence:

- Install: the download, both unpackings, the binary identified
  by `file` as a static x86-64 ELF; `--version` (2.4.1); the
  full `--help` text; the shell's descriptor limit (4096) and
  nmap's version (t00).
- Fixtures: three Python web servers started on loopback ports
  18083, 18090 and 18091, proven listening with `ss` and
  answering with curl — and a fourth listener, another tenant's
  nginx on 18084, found honestly in the same listing (t01).
- First scans: a range scan (18080–18100, greppable) finding
  the three fixtures plus the neighbour; an exact port list
  finding exactly the three; an empty stretch returning
  silence with exit 0 (t02).
- The default run: banner, the file-limit warning, four `Open`
  lines, and the default nmap follow-up failing with
  `Error Exit code = 1` while the scan's own results stood
  (t03).
- Speed: 10000 ports at batch sizes 4500 / 500 / 100 timed at
  0.80 / 0.67 / 0.62 s; a 50 ms and a 1 ms timeout still finding
  every fixture, three runs running; `--ulimit 60000` accepted
  without complaint on a root shell (t04).
- The hand-off: `nmap -A` run directly and refused
  (`Couldn't open a raw socket`); plain `nmap -sT` listing the
  three ports as `unknown`; then RustScan with `-- -sT -sV`
  showing the exact command it built and nmap identifying all
  three fixtures as SimpleHTTPServer 0.6 (Python 3.12.3); the
  bare default hand-off failing again, watched closely (t05).
- Config and options: the sample config file supplying range,
  greppable mode and batch size with no scan flags given;
  addresses read from a file; `-e 18084` excluding the
  neighbour; `--scan-order random` shuffling the output order
  (t06).
- The `--top` investigation: `--top` alone returning high
  fixture ports and taking 5.5 s against a true 1000-port
  range's 0.13 s and a full range's 6.0 s; `--top` respecting
  an explicit range; full-range scans naming a different set
  of high ghost ports each run; one ghost (53764) proven not
  a listener by `ss` and refused by curl (t06b). An annotation
  in t06 written before its output was read properly is
  corrected, in place, by a note appended to t06.
- Failures: an unresolvable hostname aborting silently in
  greppable mode (exit 1) and with a plain message without
  `-g`; a backwards range exiting 0 in silence; port 99999
  rejected by the parser (exit 2, message quoted in chapter
  6); batch size 0 exiting 0 and silently finding nothing over
  open ports (t07).
- The same first scan re-run after the fixture servers were
  stopped: silence, correctly (t08).
- The checking script: `verify-ports.py` confirming the one
  restarted fixture OPEN and the former neighbour and the
  ghost both REFUSED (t09).

Documented only — described from the project's documentation,
not run, and the text does not claim otherwise:

- Everything beyond loopback: LAN and internet targets, real
  network timing for batches and timeouts, firewalled and
  filtered behaviour, and CIDR sweeps of more than the single
  loopback address actually scanned (the address-file
  mechanism itself was run, with one loopback entry).
- UDP scanning (`--udp`): the sandbox has no UDP at all, so
  the mode is named in chapter 12 and not taught.
- The `.deb` package, Docker image and Cargo install routes of
  chapter 3, and the Windows and macOS builds.
- The default nmap follow-up's success path: it requires raw
  sockets, which this machine forbids; its failure and the
  cause are run and shown, and the working `-sT` path is the
  one taught.
- IPv6 targets (the hand-off's `{{ipversion}}` slot is quoted
  from a real run; no IPv6 scan was made), the `custom`
  scripts level, and DNS resolver options.
- The neighbour tools of chapter 11 (masscan, naabu, ZMap) —
  characterised from their documentation, not run; nmap is
  characterised from this lab's own runs plus its guide in
  this series.

Fixtures are this guide's own and deliberately generic: three
one-page web fixtures named alpha, bravo and charlie serving
stock sentences about a kettle, a workbench and a garden gate,
on loopback ports, plus the documentation example address
192.0.2.10 in one recipe. No real network, organisation or
person is scanned, named or modelled anywhere in the guide.
