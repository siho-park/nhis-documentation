"""MkDocs hook that gives every page its own search description.

A page keeps the description in its front matter if it has one, as the
generated variable pages do. Otherwise the description is the first
paragraph of the page, skipping breadcrumb lines, cut to about 160
characters. The theme inserts the description without escaping it, so it
is escaped here.
"""

import html
import re

MAX_LENGTH = 160


def first_paragraph(content):
    for match in re.finditer(r"<p>(.*?)</p>", content, re.S):
        text = " ".join(html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).split())
        if text and "›" not in text:
            return text
    return ""


def on_page_content(content, page, **kwargs):
    text = page.meta.get("description") or first_paragraph(content)
    text = " ".join(str(text).split())
    if len(text) > MAX_LENGTH:
        text = text[:MAX_LENGTH].rsplit(" ", 1)[0] + "…"
    if text:
        page.meta["description"] = html.escape(text, quote=True)
    return content
