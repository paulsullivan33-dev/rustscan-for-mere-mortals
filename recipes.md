# Recipes

Four jobs, each assembled from parts
the earlier chapters proved. All of
them scan the reader's own machines;
the first two are written for your own
computer, the third for any machine of
yours you can run RustScan on, the
fourth for the moment a result
surprises you.

## 1. The whole of your own machine

The audit this guide exists for: every
door, on the machine you are sitting
at, checked against the machine's own
account of itself.

```bash
ss -tln > before.txt
rustscan -a 127.0.0.1 -r 1-65535 -g -b 1000
ss -tln
```

Compare the scan's list with the
listeners `ss` admits to. They should
agree — except for any chapter 5
ghosts, which the comparison exposes
at once: present in the scan, absent
from `ss`, gone on a re-scan. The
lab's whole-space run took about six
seconds (transcript t06b) and turned
up two genuine neighbours alongside
the ghosts; on a machine that is
wholly yours, every surviving port
should be one you can name. Any you
cannot is the audit working.

## 2. A weekly greppable record

Put your standing settings in a
config file (chapter 9), your machines
in a targets file, and let the output
be the one-line form a file can keep:

```bash
rustscan -c ~/.rustscan.toml -a ~/targets.txt -g >> ~/scan-log.txt
```

Run weekly, the log becomes the
history of your doors: a new port
appears the week a service was
installed, and disappears the week it
was cleaned up. Two disciplines make
it trustworthy. Date each line (the
shell will: `date -Iseconds` before
the command, into the same file). And
never let silence file itself as
success without a known listener
somewhere in the targets — chapter 13
explains the failure that hides in
an unchecked silent run.

## 3. One service, closely

A scan says a door is open on a server
of yours; now you want its name and
manners. Hand that one port to nmap
through the seam:

```bash
rustscan -a 192.0.2.10 -p 8443 -- -sT -sV
```

(the address is the documentation
example — substitute your own
machine's). What comes back is
chapter 8's table for one door: the
service, its version banner, its
state. This is the daily shape of the
tool in practice: RustScan wide and
fast once, nmap narrow and deep
where it counts.

## 4. Cross-examine a surprise

Any port you did not expect, from any
recipe above, gets the chapter 5
treatment before it gets a reaction.
Here it is worked on the lab's own
ghost — port 53764, from transcript
t06b; your surprise will have its own
number, and the commands take it
exactly the same way:

```bash
ss -tln | grep 53764
curl -sv --max-time 3 http://127.0.0.1:53764/
python3 rustscan-lab/verify-ports.py "127.0.0.1 -> [53764]"
```

A listener in `ss`, an answer to curl,
an OPEN from the slow checker: a real
service, and now an identified one.
Nothing in `ss`, a refused curl, a
REFUSED from the checker, and a
re-scan that no longer names it: a
ghost, and the correct action was the
checking itself.
