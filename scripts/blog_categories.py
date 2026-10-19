"""MkDocs hook that orders the blog categories in the sidebar.

The order is taken from extra.blog_categories in mkdocs.yml, which the blog
index template (overrides/blog.html) also uses. Categories missing from that
list follow in alphabetical order.
"""

from material.plugins.blog.plugin import BlogPlugin


def on_config(config):
    order = list(config.extra.get("blog_categories") or [])

    def position(view):
        return order.index(view.name) if view.name in order else len(order)

    for plugin in config.plugins.values():
        if isinstance(plugin, BlogPlugin):
            plugin.config.categories_sort_by = position
