from __future__ import annotations

from datetime import datetime

import typer
from src.components.convert2post import ConvertPostInput
from src.components.convert2post import ConvertPostService
from src.components.pull_content import NewsInput
from src.components.pull_content import NewsService
from src.components.pull_content.type import ContentType
from src.settings.settings import load_settings

app = typer.Typer()


@app.command
def main(
    news_url: str = typer.Option([], '--url_link', '-u', help='Link to news'),
    tone: str = typer.Option('Professional', '--tone', '-t', help='Tone'),
    target_platform: str = typer.Option(
        'LinkedIn', '--target_platform', '-p', help='Target Platform',
    ),
) -> str:
    # Load settings
    settings = load_settings()

    # Initialize services
    news_service = NewsService()

    convert_post_service = ConvertPostService(
        openai_settings=settings.openai,
    )

    # Get news
    news_content = news_service.process(
        NewsInput(
            news_url=news_url,
            type=ContentType.NEWS,
        ),
    )

    # Get post
    post = convert_post_service.process(
        ConvertPostInput(
            summary_content=news_content.news_content,
            tone=tone,
            target_platform=target_platform,
        ),
    )

    # Get file_name (days + month + year)
    file_name = datetime.now().strftime('%d%m%Y')

    # Save output to file txt, file name is news_url without txt
    with open(f'{file_name}.txt', 'w', encoding='utf-8') as f:
        f.write(post.post)
    return post.post


if __name__ == '__main__':
    app()
