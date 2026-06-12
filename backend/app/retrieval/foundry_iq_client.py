"""Local knowledge-base retrieval used as a stand-in for Foundry IQ."""

from __future__ import annotations

from pathlib import Path

from app.config import settings
from app.retrieval.citation_parser import parse_markdown_excerpt
from app.schemas.responses import Citation
from app.utils.heuristics import tokenize


class LocalKnowledgeBaseClient:
    def __init__(self, knowledge_base_dir: Path | None = None) -> None:
        self.knowledge_base_dir = knowledge_base_dir or settings.knowledge_base_dir
        self.documents = self._load_documents()

    def _load_documents(self) -> list[dict[str, str | set[str]]]:
        documents: list[dict[str, str | set[str]]] = []
        for path in sorted(self.knowledge_base_dir.rglob("*.md")):
            if path.name.lower() == "readme.md":
                continue
            title, snippet = parse_markdown_excerpt(path)
            tokens = tokenize(f"{title} {snippet} {path.parent.name} {path.stem}")
            documents.append(
                {
                    "source": str(path.relative_to(settings.knowledge_base_dir.parent)),
                    "title": title,
                    "snippet": snippet,
                    "tokens": tokens,
                },
            )
        return documents

    def retrieve(self, query: str, limit: int = 2) -> list[Citation]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []

        ranked: list[tuple[int, dict[str, str | set[str]]]] = []
        for document in self.documents:
            score = len(query_tokens.intersection(document["tokens"]))  # type: ignore[arg-type]
            if score:
                ranked.append((score, document))

        ranked.sort(
            key=lambda item: (item[0], len(item[1]["snippet"])),  # type: ignore[arg-type]
            reverse=True,
        )

        return [
            Citation(
                source=document["source"],  # type: ignore[index]
                title=document["title"],  # type: ignore[index]
                snippet=document["snippet"],  # type: ignore[index]
            )
            for _, document in ranked[:limit]
        ]

