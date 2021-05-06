#!/usr/bin/env python3
# coding=utf-8

import bs4
import pytest

from literoticadownloader.chaptered_story import ChapteredStory
from literoticadownloader.pages.author_page import AuthorPage


@pytest.mark.parametrize(('test_url', 'expected_len'), (
    ('https://www.literotica.com/stories/memberpage.php?uid=910906&page=submissions', 31),
))
def test_find_single_stories(test_url: str, expected_len: int):
    test_response = AuthorPage.retrieve_resource(test_url)
    test_soup = bs4.BeautifulSoup(test_response.text, 'html.parser')
    results = AuthorPage._find_single_stories(test_soup)
    assert len(results) == expected_len


@pytest.mark.parametrize(('test_url', 'index', 'expected'), (
    ('https://www.literotica.com/stories/memberpage.php?uid=910906&page=submissions', 0, [
        'https://www.literotica.com/s/college-ponygirls-ch-01-02',
        'https://www.literotica.com/s/college-ponygirls-ch-03-04',
        'https://www.literotica.com/s/college-ponygirls-ch-05-06',
    ]),
))
def test_find_crawl_tree_for_parts(test_url: str, index: int, expected: list[str]):
    test_response = AuthorPage.retrieve_resource(test_url)
    test_soup = bs4.BeautifulSoup(test_response.text, 'html.parser')
    test_tag = test_soup.find_all('tr', attrs={'class': 'ser-ttl'})
    test_tag = test_tag[index]
    results = AuthorPage._crawl_tree_for_parts(test_tag)
    assert results == expected


@pytest.mark.parametrize(('test_url', 'expected_len'), (
    ('https://www.literotica.com/stories/memberpage.php?uid=910906&page=submissions', 2),
))
def test_find_chaptered_stories(test_url: str, expected_len: int):
    test_response = AuthorPage.retrieve_resource(test_url)
    test_soup = bs4.BeautifulSoup(test_response.text, 'html.parser')
    results = AuthorPage._find_chaptered_stories(test_soup)
    assert len(results) == expected_len
    assert all([isinstance(res, ChapteredStory) for res in results])


@pytest.mark.parametrize(('test_url', 'expected_len'), (
    ('https://www.literotica.com/stories/memberpage.php?uid=910906&page=submissions', 33),
))
def test_parse(test_url: str, expected_len: int):
    results = AuthorPage(test_url).parse()
    assert len(results) == expected_len
