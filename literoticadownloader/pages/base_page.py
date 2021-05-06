#!/usr/bin/env python3
# coding=utf-8

import logging
from abc import ABC, abstractmethod

import requests

from literoticadownloader.exceptions import LiteroticaDownloaderException
from literoticadownloader.story import Story

logger = logging.getLogger(__name__)


class BasePage(ABC):
    cookies = {
        '_pk_ses.1.dd2b': '1',
        '_pk_testcookie.1.dd2b': '1',
    }
    headers = {'User-Agent': 'Mozilla/5.0'}

    def __init__(self, url: str):
        self.url = url
        self.pages: list[requests.Response] = []

    @staticmethod
    def retrieve_resource(url: str) -> requests.Response:
        try:
            out = requests.get(url, cookies=BasePage.cookies, headers=BasePage.headers)
            return out
        except requests.exceptions.RequestException as e:
            raise LiteroticaDownloaderException(f'Failed to retrieve page {url}: {e}')

    @abstractmethod
    def _retrieve_pages(self, delay: int = 0):
        raise NotImplementedError

    @abstractmethod
    def parse(self, delay: int = 0) -> list[Story]:
        raise NotImplementedError
