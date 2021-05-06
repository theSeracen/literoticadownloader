#!/usr/bin/env python3
# coding=utf-8

import hashlib
from pathlib import Path

from ebooklib import epub


class Story:
    def __init__(self, attributes: dict[str, str], story_text: str):
        self.attributes = attributes
        self.story_text = story_text
        self.epub = epub.EpubBook()

    def create_epub(self):
        self.epub.add_author(self.attributes['author'])
        self.epub.set_title(self.attributes['title'])
        self.epub.set_language('en')
        self.epub.set_identifier(hashlib.md5(self.story_text.encode('utf-8')).hexdigest()[:6])
        chapters = self._assemble_chapters()
        [self.epub.add_item(chap) for chap in chapters]
        self.epub.add_item(epub.EpubNcx())
        self.epub.add_item(epub.EpubNav())
        style = """
@namespace epub 'http://www.idpf.org/2007/ops';
body {
    font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}
h2 {
     text-align: left;
     text-transform: uppercase;
     font-weight: 200;
}
ol {
        list-style-type: none;
}
ol > li:first-child {
        margin-top: 0.3em;
}
nav[epub|type~='toc'] > ol > li > ol  {
    list-style-type:square;
}
nav[epub|type~='toc'] > ol > li > ol > li {
        margin-top: 0.3em;
}
    """
        # add css file
        nav_css = epub.EpubItem(uid='style_nav', file_name='style/nav.css', media_type='text/css', content=style)
        self.epub.add_item(nav_css)
        self.epub.spine = ['nav', *chapters]

    def _assemble_chapters(self) -> list[epub.EpubHtml]:
        chapter = epub.EpubHtml(
            title=self.attributes['title'],
            file_name=f'{self.attributes["title"]}.xhtml',
            lang='en',
        )
        chapter.content = self.story_text
        return [chapter]

    def write_to_disk(self, destination: Path):
        write_path = self.calculate_path(destination)
        epub.write_epub(
            write_path,
            self.epub,
            {},
        )

    def calculate_path(self, destination: Path) -> Path:
        write_path = Path(destination, f'{self.attributes["title"]} - {self.attributes["author"]}.epub')
        return write_path
