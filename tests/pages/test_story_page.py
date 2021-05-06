#!/usr/bin/env python3
# coding=utf-8

import hashlib

import pytest

from literoticadownloader.pages.story_page import StoryPage
from literoticadownloader.story import Story


@pytest.mark.parametrize(('test_url', 'expected_hash'), (
    ('https://literotica.com/s/the-pet-girl-shoppe', '5e00db419fc127cccc12e13ed2ff9ddb'),
))
def test_parse_for_story(test_url: str, expected_hash: str):
    test_response = StoryPage.retrieve_resource(test_url)
    result = StoryPage._parse_for_story(test_response)
    result_hash = hashlib.md5(result.encode('utf-8'))
    assert result_hash.hexdigest() == expected_hash


@pytest.mark.parametrize(('test_url', 'expected_dict'), (
    ('https://literotica.com/s/the-pet-girl-shoppe', {
        'title': 'The Pet Girl Shoppe',
        'author': 'Sarahcheer',
        'tags': {'science fiction erotica', 'science fiction bdsm'}
    }),
))
def test_extract_attributes(test_url: str, expected_dict: dict[str, str]):
    test_response = StoryPage.retrieve_resource(test_url)
    result = StoryPage._extract_attributes(test_response)
    assert all([result[key] == expected_dict[key] for key in expected_dict.keys()])


@pytest.mark.parametrize(('test_url', 'expected_story_hash'), (
    ('https://literotica.com/s/the-pet-girl-shoppe', '42cf5f19302391c442e7f37e36ed6023'),
))
def test_parse_to_story(test_url: str, expected_story_hash: str):
    test_story = StoryPage(test_url)
    result = test_story.parse()
    assert isinstance(result, Story)
    story_content_hash = hashlib.md5(result.story_text.encode('utf-8'))
    assert story_content_hash.hexdigest() == expected_story_hash
