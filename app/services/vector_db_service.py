"""Vector DB Service — wraps VectorDB for semantic search over politician data."""

import logging
from typing import Any, Dict, List, Optional

from app.core.vector_db import VectorDB

logger = logging.getLogger(__name__)


class VectorDBService:
    """Thin service layer over ChromaDB for politician semantic search."""

    def __init__(self) -> None:
        self.vdb = VectorDB()

    def count(self) -> int:
        return self.vdb.count()

    def search(
        self,
        query: str,
        n_results: int = 5,
        politician_type: Optional[str] = None,
        state: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Run semantic search and return a flat list of result dicts."""
        where: Dict[str, Any] = {}
        if politician_type:
            where["type"] = politician_type
        if state:
            where["state"] = state

        results = self.vdb.query(
            query_text=query,
            n_results=n_results,
            where=where if where else None,
        )

        items: List[Dict[str, Any]] = []
        if not results or not results.get("ids"):
            return items

        ids = results["ids"][0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]
        for i, pid in enumerate(ids):
            items.append(
                {
                    "id": pid,
                    "document": docs[i] if i < len(docs) else "",
                    "metadata": metas[i] if i < len(metas) else {},
                    "distance": distances[i] if i < len(distances) else None,
                }
            )

        return items
