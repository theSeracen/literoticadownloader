#!/usr/bin/env python3
# coding=utf-8

from ebooklib import epub

from literoticadownloader.pages.story_page import StoryPage
from literoticadownloader.story import Story


class ChapteredStory(Story):
    def __init__(self, attributes: dict, part_urls: list[str]):
        super(ChapteredStory, self).__init__(attributes, '')
        self.part_urls = part_urls
        self.sub_stories: list[Story] = []

    def _get_parts(self):
        story_parts = [StoryPage(url) for url in self.part_urls]
        story_parts = [part.parse()[0] for part in story_parts]
        self.sub_stories = story_parts

    def _assemble_chapters(self) -> list[epub.EpubHtml]:
        self._get_parts()
        out = []
        for part in self.sub_stories:
            chapter = part._assemble_chapters()[0]
            out.append(chapter)
        return out
