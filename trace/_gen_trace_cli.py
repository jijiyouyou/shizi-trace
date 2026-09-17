# -*- coding: utf-8 -*-
"""Assemble tools/trace/trace.cli from mau / iparser / eparser_pe scripts."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _die_case(arg_label: str) -> str:
    """Shared die→uniq mapping; arg_label is for error text (e.g. arg2 / arg5)."""
    return (
        f'case $die xdie "local uniq 0x90; local ok 1" '
        f"sdie8 \"case $pipe pp0 'local uniq 0x80; local ok 1' pp1 'local uniq 0x81; local ok 1'\" "
        f"sdie0 \"case $pipe pp0 'local uniq 0x00; local ok 1' pp1 'local uniq 0x01; local ok 1'\" "
        f"sdie1 \"case $pipe pp0 'local uniq 0x10; local ok 1' pp1 'local uniq 0x11; local ok 1'\" "
        f"sdie2 \"case $pipe pp0 'local uniq 0x20; local ok 1' pp1 'local uniq 0x21; local ok 1'\" "
        f"sdie3 \"case $pipe pp0 'local uniq 0x30; local ok 1' pp1 'local uniq 0x31; local ok 1'\" "
        f"sdie4 \"case $pipe pp0 'local uniq 0x40; local ok 1' pp1 'local uniq 0x41; local ok 1'\" "
        f"sdie5 \"case $pipe pp0 'local uniq 0x50; local ok 1' pp1 'local uniq 0x51; local ok 1'\" "
        f"sdie6 \"case $pipe pp0 'local uniq 0x60; local ok 1' pp1 'local uniq 0x61; local ok 1'\" "
        f"sdie7 \"case $pipe pp0 'local uniq 0x70; local ok 1' pp1 'local uniq 0x71; local ok 1'\" "
        f'* "echo ERROR: {arg_label} must be xdie or sdie0..sdie8; local ok 0"'
    )


def main() -> None:
    mau = (ROOT / "mau_trace.cli").read_text(encoding="utf-8")
    iparser = (ROOT / "iparser_trace.cli").read_text(encoding="utf-8")
    eparser = (ROOT / "eparser_pe_trace.cli").read_text(encoding="utf-8")

    mau_for = next(ln for ln in mau.splitlines() if ln.startswith("for mau="))

    ip_lines = iparser.splitlines()
    ip_start = next(i for i, ln in enumerate(ip_lines) if "---- iparser start ----" in ln)
    ip_body_lines = [
        ln
        for ln in ip_lines[ip_start:]
        if ln.strip() and not ln.strip().startswith("#")
    ]
    ip_inner = "; ".join(ip_body_lines)
    iparser_gated = (
        "case $ok 0 \"echo skip iparser; local ip_hi -1\"\n"
        "case $ok 1 \"echo iparser_trace run; local ip_hi 0\"\n"
        f"for ip=0,${{ip_hi}} '{ip_inner}'"
    )

    ep_lines = eparser.splitlines()
    ep_start = next(i for i, ln in enumerate(ep_lines) if ln.startswith("for mod="))
    eparser_body = "\n".join(ep_lines[ep_start:])

    parts: list[str] = []
    parts.append(
        """# trace.cli — 合并 mau_trace + iparser_trace + eparser_pe_trace
# 用法:
#   trace.cli ipp <die> <pp0|pp1> epp <die> <pp0|pp1>
# 例:
#   trace.cli ipp xdie pp0 epp sdie8 pp1
# 行为:
#   ipp: mau0..mau8 + iparser
#   epp: mau9..mau10 + eparser + pedt
# die: xdie | sdie0..sdie8

echo $1
echo $2
echo $3
echo $4
echo $5
echo $6

local run_ipp 0
local run_epp 0
case $1 ipp "local run_ipp 1; echo arg1=ipp" * "echo ERROR: arg1 must be ipp; local run_ipp 0"
case $4 epp "local run_epp 1; echo arg4=epp" * "echo ERROR: arg4 must be epp; local run_epp 0"

# ======================== IPP: mau0-8 + iparser ========================
echo ---- ipp start ----
local die $2
local pipe $3
local ok 0
local mau_lo 0
local mau_hi -1
local pp 0
local uniq 0x90
local ip_hi -1
case $run_ipp 0 "echo skip ipp section; local ok 0; local mau_hi -1; local ip_hi -1"
case $run_ipp 1 "case $pipe pp0 'local pp 0; local mau_lo 0; local mau_hi 8; echo ipp pipe=pp0' pp1 'local pp 1; local mau_lo 0; local mau_hi 8; echo ipp pipe=pp1' * 'echo ERROR: arg3 must be pp0 or pp1; local mau_hi -1'"
"""
    )
    parts.append(_die_case("arg2"))
    parts.append(
        """case $run_ipp 0 "local ok 0; local mau_hi -1; local ip_hi -1"
case $ok 0 "echo ipp aborted; local mau_hi -1; local ip_hi -1"
case $ok 1 "echo ipp mau=${mau_lo}..${mau_hi} uniq=$uniq"
echo "ipp: die=$die pipe=$pipe pp=$pp uniq=$uniq ok=$ok mau=${mau_lo}..${mau_hi} run_ipp=$run_ipp"
"""
    )
    parts.append(mau_for)
    parts.append("")
    parts.append(iparser_gated)
    parts.append("echo ---- ipp end ----")
    parts.append("")
    parts.append(
        """# ======================== EPP: mau9-10 + eparser + pedt ========================
echo ---- epp start ----
local die $5
local pipe $6
local ok 0
local mau_lo 9
local mau_hi -1
local pp 0
local uniq 0x90
local ep_hi -1
local pd_hi -1
case $run_epp 0 "echo skip epp section; local ok 0; local mau_hi -1; local ep_hi -1; local pd_hi -1"
case $run_epp 1 "case $pipe pp0 'local pp 0; local mau_lo 9; local mau_hi 10; local ep_hi 0; local pd_hi 1; echo epp pipe=pp0' pp1 'local pp 1; local mau_lo 9; local mau_hi 10; local ep_hi 0; local pd_hi 1; echo epp pipe=pp1' * 'echo ERROR: arg6 must be pp0 or pp1; local mau_hi -1; local ep_hi -1; local pd_hi -1'"
"""
    )
    parts.append(_die_case("arg5"))
    parts.append(
        """case $run_epp 0 "local ok 0; local mau_hi -1; local ep_hi -1; local pd_hi -1"
case $ok 0 "echo epp aborted; local mau_hi -1; local ep_hi -1; local pd_hi -1"
case $ok 1 "echo epp mau=${mau_lo}..${mau_hi} uniq=$uniq"
echo "epp: die=$die pipe=$pipe pp=$pp uniq=$uniq ok=$ok mau=${mau_lo}..${mau_hi} run_epp=$run_epp"
"""
    )
    parts.append(mau_for)
    parts.append("")
    parts.append('case $ok 0 "echo skip eparser_pe"')
    parts.append('case $ok 1 "echo eparser_pe_trace run"')
    parts.append(eparser_body)
    parts.append("echo ---- epp end ----")
    parts.append("")

    text = "\n".join(parts)
    out = ROOT / "trace.cli"
    out.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {out} ({out.stat().st_size} bytes, {len(text.splitlines())} lines)")


if __name__ == "__main__":
    main()
