#!/usr/bin/env python3
# coding=utf-8

import itertools
import logging

import bs4

from literoticadownloader.chaptered_story import ChapteredStory
from literoticadownloader.pages.base_page import BasePage
from literoticadownloader.pages.story_page import StoryPage
from literoticadownloader.story import Story

logger = logging.getLogger(__name__)


class AuthorPage(BasePage):
    def __init__(self, url: str):
        super(AuthorPage, self).__init__(url)

    def parse(self, delay: int = 0) -> list[Story]:
        self._retrieve_pages()
        soup = bs4.BeautifulSoup(self.pages[0].text, 'html.parser')
        single_story_urls = self._find_single_stories(soup)

        logger.debug(f'Found {len(single_story_urls)} single story URLs')
        logger.info(f'Fetching stories for URL {self.url}')

        single_story_pages = [StoryPage(url) for url in single_story_urls]
        single_stories = []
        for page in single_story_pages:
            single_stories.append(page.parse(delay))
        chaptered_stories = self._find_chaptered_stories(soup)
        logger.debug(f'Found {len(chaptered_stories)} chaptered stories')
        return list(itertools.chain(*single_stories, chaptered_stories))

    @staticmethod
    def _find_single_stories(soup: bs4.BeautifulSoup) -> list[str]:
        out = []
        root_story_tags = soup.find_all('tr', attrs={'class': 'root-story'})
        for tag in root_story_tags:
            link = tag.find('a', attrs={'class': 't-t84'}).get('href')
            out.append(link)
        return out

    @staticmethod
    def _find_chaptered_stories(soup: bs4.BeautifulSoup) -> list[ChapteredStory]:
        author = soup.find('a', attrs={'class': 'contactheader'}).text
        out = []
        titles = soup.find_all('tr', attrs={'class': 'ser-ttl'})
        for title in titles:
            story_title = title.text
            result = AuthorPage._crawl_tree_for_parts(title)
            out.append(ChapteredStory({'title': story_title, 'author': author}, result))
        return out

    @staticmethod
    def _crawl_tree_for_parts(title_tag: bs4.Tag) -> list[str]:
        chapters = []
        current_tag = title_tag.next_sibling
        while 'sl' in current_tag.get('class'):
            link = current_tag.find('a', attrs={'class': 'bb'}).get('href')
            chapters.append(link)
            current_tag = current_tag.next_sibling
        return chapters

    def _retrieve_pages(self, delay: int = 0):
        self.pages.append(self.retrieve_resource(self.url))
