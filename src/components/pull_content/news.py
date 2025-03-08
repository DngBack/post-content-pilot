from __future__ import annotations

import re
from urllib.parse import urljoin
from urllib.parse import urlparse

import html2text
import requests
from bs4 import BeautifulSoup

from .base import ContentParserInput
from .base import ContentParserOutput
from .base import ContentParserService


class NewsInput(ContentParserInput):
    news_url: str


class NewsOutput(ContentParserOutput):
    news_content: str


class NewsService(ContentParserService):
    def process(self, inputs: NewsInput) -> NewsOutput:
        markdown_content = self._get_markdown_content(
            news_url=inputs.news_url,
            include_images=False,
            include_links=False,
        )
        processed_content = self._post_process(
            markdown_content=markdown_content,
            start_at_first_h1=True,
        )
        return NewsOutput(news_content=processed_content)

    def _post_process(self, markdown_content: str, start_at_first_h1: bool = True) -> str:
        # Clean up the markdown
        markdown = markdown_content.replace('\n\n\n\n', '\n\n')

        # Post-processing: Remove all content before the first H1 header if requested
        if start_at_first_h1:
            # Look for the first proper Markdown H1 header (# at the start of a line)
            h1_match = re.search(r'^\s*# .+', markdown, re.MULTILINE)
            if h1_match:
                # Keep only the content starting from the first H1 header
                markdown = markdown[h1_match.start():]

        return markdown

    def _get_markdown_content(self, news_url: str, include_images: bool = False, include_links: bool = False) -> str:
        # Validate URL
        if not news_url.startswith(('http://', 'https://')):
            news_url = 'https://' + news_url

        # Make request with a realistic user agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

        response = requests.get(news_url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script in soup(['script', 'style']):
            script.decompose()

        # Configure html2text
        converter = html2text.HTML2Text()
        converter.ignore_links = not include_links
        converter.ignore_images = not include_images
        converter.body_width = 0  # Don't wrap text
        converter.protect_links = True  # Don't convert links to references

        # Fix relative URLs if needed
        if include_links or include_images:
            base_url = '{0.scheme}://{0.netloc}'.format(urlparse(news_url))

            # Fix relative links
            if include_links:
                for a_tag in soup.find_all('a', href=True):
                    if not a_tag['href'].startswith(('http://', 'https://', 'mailto:', 'tel:')):
                        a_tag['href'] = urljoin(base_url, a_tag['href'])

            # Fix relative image sources
            if include_images:
                for img_tag in soup.find_all('img', src=True):
                    if not img_tag['src'].startswith(('http://', 'https://', 'data:')):
                        img_tag['src'] = urljoin(base_url, img_tag['src'])

        # Convert to markdown
        markdown = converter.handle(str(soup))
        return markdown
