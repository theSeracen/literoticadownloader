#!/usr/bin/env python3
# coding=utf-8
from argparse import Namespace
from pathlib import Path

import pytest

import literoticadownloader.__main__ as main


@pytest.fixture()
def args(tmp_path: Path) -> Namespace:
    args = Namespace()
    args.verbose = 1
    args.destination = tmp_path
    args.link = ''
    args.delay = 0
    return args


@pytest.mark.parametrize(('test_link', 'expected_len'), (
    ('https://www.literotica.com/stories/memberpage.php?uid=1303092&page=submissions', 1),
    ('https://www.literotica.com/stories/memberpage.php?uid=910906&page=submissions', 33),
))
def test_integration_author_page(test_link: str, expected_len: int, args: Namespace, capsys: pytest.CaptureFixture):
    args.link = test_link
    main.main(args)
    out = capsys.readouterr()
    assert out.err.count('Story written to') == expected_len


@pytest.mark.parametrize(('test_link', 'expected_len'), (
    ('https://www.literotica.com/s/the-lead', 1),
    ('https://www.literotica.com/s/bitchsuited-punishment', 1)
))
def test_integration_story_page(test_link: str, expected_len: int, args: Namespace, capsys: pytest.CaptureFixture):
    args.link = test_link
    main.main(args)
    out = capsys.readouterr()
    assert out.err.count('Story written to') == expected_len
