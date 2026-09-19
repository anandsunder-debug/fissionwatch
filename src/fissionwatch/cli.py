"""Command line interface for fissionwatch."""

from __future__ import annotations

import argparse

from ._version import __version__
from .customer import customer_experience_quality, reliability_adjusted_sri


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fissionwatch")
    subcommands = parser.add_subparsers(dest="command")

    subcommands.add_parser("version", help="print the installed package version")

    ceq_parser = subcommands.add_parser("ceq", help="compute customer experience quality")
    ceq_parser.add_argument("--availability", type=float, required=True)
    ceq_parser.add_argument("--latency-s", type=float, required=True)
    ceq_parser.add_argument("--error-rate", type=float, required=True)
    ceq_parser.add_argument("--functional-quality", type=float, default=1.0)
    ceq_parser.add_argument("--recovery-quality", type=float, default=1.0)
    ceq_parser.add_argument("--latency-ref-s", type=float, default=1.0)
    ceq_parser.add_argument("--error-ref", type=float, default=0.01)

    rsri_parser = subcommands.add_parser("rsri", help="compute reliability-adjusted SRI")
    rsri_parser.add_argument("--rho", type=float, required=True)
    rsri_parser.add_argument("--sigma-star", type=float, required=True)
    rsri_parser.add_argument("--cia", type=float, required=True)
    rsri_parser.add_argument("--alpha", type=float, default=1.0)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "version":
        print(__version__)
        return 0
    if args.command == "ceq":
        value = customer_experience_quality(
            availability=args.availability,
            latency_s=args.latency_s,
            error_rate=args.error_rate,
            functional_quality=args.functional_quality,
            recovery_quality=args.recovery_quality,
            latency_ref_s=args.latency_ref_s,
            error_ref=args.error_ref,
        )
        print(f"{value:.6f}")
        return 0
    if args.command == "rsri":
        value = reliability_adjusted_sri(args.rho, args.sigma_star, args.cia, alpha=args.alpha)
        print(f"{value:.6f}")
        return 0

    parser.print_help()
    return 0
