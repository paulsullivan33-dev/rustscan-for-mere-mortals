#!/usr/bin/env python3
"""Re-check a RustScan greppable result, one plain connection at a time.

Usage: python3 verify-ports.py "127.0.0.1 -> [18083,18090]"
Prints each port as OPEN (something accepted a connection just now)
or REFUSED (nothing did). A port the scan reported but this script
calls REFUSED was most likely a loopback ghost - see chapter 5.
"""
import socket
import sys

def main() -> int:
    if len(sys.argv) != 2 or "->" not in sys.argv[1]:
        print(__doc__)
        return 2
    host, _, rest = sys.argv[1].partition("->")
    host = host.strip()
    ports = [int(p) for p in rest.strip().strip("[]").split(",") if p.strip()]
    for port in ports:
        sock = socket.socket()
        sock.settimeout(2)
        try:
            sock.connect((host, port))
            print(f"{host}:{port} OPEN")
        except OSError as exc:
            print(f"{host}:{port} REFUSED ({exc.__class__.__name__})")
        finally:
            sock.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
