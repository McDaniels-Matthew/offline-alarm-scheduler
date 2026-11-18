#!/usr/bin/env python3
"""Pre-publication heuristic audit of Git-tracked files; intentionally conservative.

This is not legal review, a secret scanner or a substitute for checking Git history.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import subprocess
import sys

FORBIDDEN_DIRS={'firmware','ghidra','captures','flash','backups','backup','usb','local','archives','dump','dumps'}
FORBIDDEN_EXT={'.bin','.elf','.hex','.img','.dfu','.cpio','.dat','.gpr','.rep','.gzf','.har','.pcap','.pcapng','.key','.pem','.p12','.pfx','.kdbx'}
FORBIDDEN_NAMES={'firmware','nanu-arc-combined.bin.c','pasted text.txt','.env','id_rsa','id_ed25519'}
MAX_SIZE=300_000


def paths_to_check(root:Path)->list[Path]:
    p=subprocess.run(['git','ls-files','-z'],cwd=root,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode==0:
        return [root/Path(x.decode('utf-8','replace')) for x in p.stdout.split(b'\x00') if x]
    return [p for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts and '__pycache__' not in p.relative_to(root).parts]

def audit(root:Path)->list[str]:
    failures=[]
    for path in paths_to_check(root):
        rel=path.relative_to(root)
        low=rel.as_posix().lower()
        if any(part.lower() in FORBIDDEN_DIRS for part in rel.parts[:-1]):failures.append(f'PROHIBITED PATH: {low}')
        if path.suffix.lower() in FORBIDDEN_EXT or path.name.lower() in FORBIDDEN_NAMES or low.endswith('.bin.c'):
            failures.append(f'PROHIBITED FILE: {low}')
        if not path.exists(): failures.append(f'MISSING TRACKED FILE: {low}');continue
        blob=path.read_bytes()
        if len(blob)>MAX_SIZE:failures.append(f'UNUSUALLY LARGE FILE: {low} ({len(blob)} bytes)')
        if b'\x00' in blob:failures.append(f'BINARY CONTENT: {low}')
        # Deliberate broad patterns; false positives are reasons for manual review.
        for token in (b'-----BEGIN '+b'PRIVATE KEY-----', b'gh'+b'p_', b'github'+b'_pat_', b'AK'+b'IA'):
            if token in blob:failures.append(f'POSSIBLE SECRET: {low} ({token[:6].decode("ascii","replace")})')
    return failures

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path.cwd())
    ns=ap.parse_args();root=ns.root.resolve()
    bad=audit(root)
    if bad:
        print('Publication audit requires review:',*bad,sep='\n - ',file=sys.stderr);return 1
    print(f'Heuristic file audit passed: {len(paths_to_check(root))} files in {root}')
    print('Still inspect staged diffs and entire Git history; this tool is not legal clearance.')
    return 0
if __name__=='__main__':raise SystemExit(main())
