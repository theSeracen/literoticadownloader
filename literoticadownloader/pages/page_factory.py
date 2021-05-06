#!/usr/bin/env python3
# coding=utf-8

import logging
from typing import Type

from literoticadownloader.exceptions import LiteroticaDownloaderException
from literoticadownloader.pages.author_page import AuthorPage
from literoticadownloader.pages.base_page import BasePage
from literoticadownloader.pages.story_page import StoryPage

logger = logging.getLogger(__name__)


class PageFactory:
    @staticmethod
    def pull_lever(url: str) -> Type[BasePage]:
        if 'memberpage' in url:
            return AuthorPage
        elif '/s/' in url:
            return StoryPage
        else:
            raise LiteroticaDownloaderException(f'No module for {url}')
