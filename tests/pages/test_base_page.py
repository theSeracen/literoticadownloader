#!/usr/bin/env python3
# coding=utf-8

import pytest

from literoticadownloader.pages.base_page import BasePage


@pytest.mark.parametrize('test_url', (
    'https://literotica.com/s/the-pet-girl-shoppe',
))
def test_retrieve_page(test_url: str):
    result = BasePage.retrieve_resource(test_url)
    assert result.status_code == 200
