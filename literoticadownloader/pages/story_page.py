#!/usr/bin/env python3
# coding=utf-8

import logging
import re
import time

import bs4
import requests

from literoticadownloader.exceptions import LiteroticaDownloaderException
from literoticadownloader.pages.base_page import BasePage
from literoticadownloader.story import Story

logger = logging.getLogger(__name__)


class StoryPage(BasePage):
    def __init__(self, url: str):
        super(StoryPage, self).__init__(url)
        self.raw_story_parts: list[str] = []

    def _retrieve_pages(self, delay: int = 0):
        i = 1
        while True:
            url = self.url
            url += f'?page={i}'
            url += '#tab__tags'
            logger.debug(f'Retrieving page {url}')
            time.sleep(delay)
            response = self.retrieve_resource(url)
            if response.status_code == 404:
                break
            elif response.status_code == 200:
                self.pages.append(response)
                i += 1
            else:
                raise LiteroticaDownloaderException(f'URL {url} returned with status code {response.status_code}')

    def parse(self, delay: int = 0) -> list[Story]:
        self._retrieve_pages(delay)
        story_parts = [self._parse_for_story(page) for page in self.pages]
        attributes = self._extract_attributes(self.pages[0])
        story_parts = '\n'.join(story_parts)
        out = Story(attributes, story_parts)
        return [out]

    @staticmethod
    def _parse_for_story(page: requests.Response) -> str:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        story = soup.find('div', attrs={'class': 'aa_ht'})
        story = list(story.children)[0]
        return story.prettify()

    @staticmethod
    def _extract_attributes(page: requests.Response) -> dict:
        soup = bs4.BeautifulSoup(page.text, 'html.parser')
        out = {
            'title': soup.find('h1', attrs={'class': re.compile('headline')}).text,
            'author': soup.find('a', attrs={'class': 'y_eU'}).text,
            'tags': StoryPage._extract_tags(soup),
        }
        return out

    @staticmethod
    def _extract_tags(soup: bs4.BeautifulSoup) -> set[str]:
        tags = soup.find_all('a', attrs={'class': 'av_as av_r'})
        tags = [tag.text for tag in tags]
        return set(tags)
