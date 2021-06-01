from dataclasses import dataclass, field


@dataclass()
class Article:
    article_id: str
    timestamp: str
    author: str
    headline: str
    excerpt: str
    text: str
    nouns: dict = field(default_factory=lambda: {})
    nounScore: dict = field(default_factory=lambda: {})

    def __hash__(self):
        return hash(self.article_id)
