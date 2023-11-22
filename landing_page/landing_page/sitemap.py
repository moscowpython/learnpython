import datetime

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from mainpage.utils.github import fetch_last_commit_date_from_github_repo


class LearnSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self) -> list[str]:
        return ["index", "index_advanced"]

    def location(self, item: str) -> str:
        return reverse(item)

    def lastmod(self, obj: str) -> datetime.datetime | None:
        return fetch_last_commit_date_from_github_repo('moscowpython', 'learnpython')
