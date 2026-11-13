"""Command-line entry point for running the simulator without ROS 2."""

import argparse
import json
import sys
from typing import Optional, Sequence

from warehouse_bot.simulator import WarehouseSimulator


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description='Run the warehouse robot simulator')
    parser.add_argument('--max-steps', type=int, default=500, help='Maximum simulation steps')
    parser.add_argument('--jsonl', help='Append telemetry JSON Lines to this file instead of stdout')
    args = parser.parse_args(argv)
    if args.max_steps <= 0:
        parser.error('--max-steps must be positive')

    simulator = WarehouseSimulator()
    stream = open(args.jsonl, 'a', encoding='utf-8') if args.jsonl else sys.stdout
    try:
        for _ in range(args.max_steps):
            event = simulator.step()
            print(json.dumps(event, sort_keys=True), file=stream, flush=True)
            if simulator.finished:
                return 0
        return 0 if simulator.finished else 2
    finally:
        if args.jsonl:
            stream.close()


if __name__ == '__main__':
    raise SystemExit(main())
