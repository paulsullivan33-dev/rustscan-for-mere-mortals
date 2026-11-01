# Installing RustScan

You finish this chapter with RustScan
on your machine, from the project's
official release, and a version line
that proves it runs.

RustScan is one small static binary —
it carries what it needs with it — so
installing is mostly *fetching the
right file and putting it somewhere on
your path*. The project publishes its
releases on its GitHub page (the
project moved house; the current home
is `github.com/bee-san/RustScan`, and
the old address redirects there). The
lab installed **2.4.1**, the current
release as this guide was written,
from the official release page.

## The binary route (what the lab did)

For 64-bit Linux, the release offers
`x86_64-linux-rustscan.tar.gz.zip` —
yes, a zip around a tarball; both
layers are ordinary:

```bash
curl -LO https://github.com/bee-san/RustScan/releases/download/2.4.1/x86_64-linux-rustscan.tar.gz.zip
unzip x86_64-linux-rustscan.tar.gz.zip
tar -xzf x86_64-linux-rustscan.tar.gz
```

Inside is a single file, `rustscan`.
Transcript t00 records the whole
fetch. The check that proves the
install is the version:

```bash
./rustscan --version
```

```text
rustscan 2.4.1
```

Move the binary somewhere on your path
(a `~/bin` folder you already use, or
`/usr/local/bin` with sudo) and the
rest of this guide calls it plain
`rustscan`.

## The package route

The same release page offers
`rustscan.deb.zip` for Debian and
Ubuntu: unzip it, then install the
`.deb` inside with your package
manager (`sudo apt install ./rustscan_*.deb`
once unzipped). The project also
documents a Docker image and building
with Cargo, Rust's package manager
(`cargo install rustscan`). Those
routes are described from the project
documentation, not run in this lab —
the binary above is the one every
transcript here used — but they end at
the same `--version` check, and that
check is the point of the chapter:
whichever road you took, arrive at a
version line before you scan anything.

## The companion: nmap

RustScan's second stage needs **nmap**
installed, or the follow-up has
nothing to run. On Debian and Ubuntu,
`sudo apt install nmap`; on other
systems, your package manager or
nmap.org. The lab's machine already
had it:

```bash
nmap --version | head -2
```

```text
Nmap version 7.94SVN ( https://nmap.org )
Platform: x86_64-pc-linux-gnu
```

If nmap is missing, RustScan still
scans — the greppable mode of chapter
4 works fine — but the default run's
follow-up step will fail, and chapter
13 lists that failure among its usual
suspects.

## Two checks before your first scan

```bash
ulimit -n        # your file-descriptor limit
rustscan --help  # the whole flag list, one screen
```

The lab's limit was **4096**, below
RustScan's default batch of 4500, and
the first default scan warned about
it. Seeing the number now turns that
warning from a surprise into a
recognition. The help text is worth
one full read before chapter 4: this
guide uses most of it, and it is
short.
