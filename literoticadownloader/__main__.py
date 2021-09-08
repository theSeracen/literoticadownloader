#!/usr/bin/env python3

import argparse
import logging
import sys
from pathlib import Path

from literoticadownloader.pages.page_factory import PageFactory

logger = logging.getLogger()
parser = argparse.ArgumentParser()


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    if verbosity > 0:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)


def _add_arguments():
    parser.add_argument('destination', type=str)
    parser.add_argument('link', type=str)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('-d', '--delay', type=int, default=0)


def main(args: argparse.Namespace):
    _setup_logging(args.verbose)
    args.destination = Path(args.destination).expanduser().resolve()
    page_module = PageFactory.pull_lever(args.link)

    logger.debug(f'Using module {page_module.__name__}')
    if args.delay:
        logger.info(f'Using a delay of {args.delay} seconds')
    stories = page_module(args.link).parse(args.delay)

    if not args.destination.exists():
        logger.warning(f'Destination {args.destination} does not exist, creating it')
        args.destination.mkdir(exist_ok=True, parents=True)

    for story in stories:
        story.create_epub()
        story.write_to_disk(args.destination)
        logger.info(f'Story written to {story.calculate_path(args.destination)}')


if __name__ == '__main__':
    _add_arguments()
    args = parser.parse_args()
    main(args)
