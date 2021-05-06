#!/usr/bin/env python3
# coding=utf-8

from typing import Type

import pytest

from literoticadownloader.pages.author_page import AuthorPage
from literoticadownloader.pages.base_page import BasePage
from literoticadownloader.pages.page_factory import PageFactory
from literoticadownloader.pages.story_page import StoryPage


@pytest.mark.parametrize(('test_url', 'expected'), (
    ('https://www.literotica.com/s/human-furniture-company', StoryPage),
    ('https://www.literotica.com/stories/memberpage.php?uid=910906&page=submissions', AuthorPage)
))
def test_pull_lever(test_url, expected: Type[BasePage]):
    result = PageFactory.pull_lever(test_url)
    assert result == expected
