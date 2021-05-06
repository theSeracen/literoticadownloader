#!/usr/bin/env python3
# coding=utf-8

import hashlib
from pathlib import Path

import pytest

from literoticadownloader.pages.story_page import StoryPage
from literoticadownloader.story import Story


def test_create_epub(tmp_path: Path):
    test_content = '<p>test string</p>'
    test_attributes = {'title': 'Test', 'author': 'Author'}
    test_story = Story(test_attributes, test_content)
    test_story.create_epub()
    test_story.write_to_disk(tmp_path)
    test_path = Path(tmp_path, 'Test - Author.epub')
    assert test_path.exists()


@pytest.mark.parametrize('test_url', (
    'https://literotica.com/s/the-pet-girl-shoppe',
))
def test_create_full_story(test_url: str, tmp_path: Path):
    test_story = StoryPage(test_url)
    test_story._retrieve_pages()
    test_story = test_story.parse()
    test_story.create_epub()
    test_story.write_to_disk(tmp_path)
    test_path = test_story._calculate_path(tmp_path)
    assert test_path.exists()
