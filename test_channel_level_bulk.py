#!/usr/bin/env python3
"""
Live test for the ILV bulk speaker channel level support (SpeakerChannelLevelBulk).

Run against your real VSX-924 (or any Pioneer/Onkyo AVR) before trusting this code
or opening a PR. Does NOT touch anything unless you pass --set.

Usage:
    python test_channel_level_bulk.py --host 192.168.1.50
    python test_channel_level_bulk.py --host 192.168.1.50 --set SW -6.0
"""
# pylint: disable=import-error,broad-except

import argparse
import asyncio
import logging

from aiopioneer import PioneerAVR
from aiopioneer.const import Zone

_LOGGER = logging.getLogger(__name__)


async def main(args: argparse.Namespace) -> bool:
    """Connect, query model + bulk channel levels, optionally set one channel."""
    pioneer = PioneerAVR(args.host)

    try:
        await pioneer.connect()
    except Exception as exc:
        print(f"Could not connect to AVR: {exc!r}")
        return False

    await pioneer.query_device_info()
    print(f"AVR model: {pioneer.properties.amp.get('model')}")

    print("\n--- Trying CLV (per-channel) query first, for comparison ---")
    try:
        result = await pioneer.send_command(
            "query_channel_level", "all", zone=Zone.Z1, ignore_error=True
        )
        print(f"query_channel_level (CLV) result: {result!r}")
    except Exception as exc:
        print(f"query_channel_level (CLV) raised: {exc!r}")

    print("\n--- Trying ILV (bulk) query ---")
    try:
        result = await pioneer.send_command(
            "query_channel_level_bulk", zone=Zone.Z1, ignore_error=True
        )
        print(f"query_channel_level_bulk (ILV) result: {result!r}")
    except Exception as exc:
        print(f"query_channel_level_bulk (ILV) raised: {exc!r}")

    print(f"\nDecoded channel_level property: {pioneer.properties.channel_level}")

    if args.set:
        channel, level = args.set[0], float(args.set[1])
        print(f"\n--- Setting {channel} to {level}dB via ILV ---")
        try:
            result = await pioneer.send_command(
                "set_channel_level_bulk", channel, level, zone=Zone.Z1
            )
            print(f"set_channel_level_bulk result: {result!r}")
            print(f"channel_level after set: {pioneer.properties.channel_level}")
        except Exception as exc:
            print(f"set_channel_level_bulk raised: {exc!r}")

    await pioneer.shutdown()
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True, help="AVR IP address or hostname")
    parser.add_argument(
        "--set",
        nargs=2,
        metavar=("CHANNEL", "LEVEL_DB"),
        help="Also SET a channel level, e.g. --set SW -6.0 (only base-12 channels "
        "are settable: L R C SL SR SBL SBR SW FHL FHR FWL FWR)",
    )
    parsed_args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    rc = asyncio.run(main(parsed_args))
    exit(0 if rc else 1)
