"""Unit tests for VectorDBService."""

import sys
from unittest.mock import MagicMock

# fastembed and chromadb are C-extension packages not installed in the test venv;
# mock them before the import chain loads them.
for _mod in ("fastembed", "chromadb", "chromadb.api", "chromadb.api.types"):
    sys.modules.setdefault(_mod, MagicMock())

from app.services.vector_db_service import VectorDBService  # noqa: E402


def _make_service(query_result=None):
    svc = VectorDBService.__new__(VectorDBService)
    svc.vdb = MagicMock()
    svc.vdb.count.return_value = 42
    if query_result is not None:
        svc.vdb.query.return_value = query_result
    return svc


def _chroma_result(ids, docs, metas, distances):
    return {
        "ids": [ids],
        "documents": [docs],
        "metadatas": [metas],
        "distances": [distances],
    }


class TestCount:
    def test_delegates_to_vdb(self):
        svc = _make_service()
        assert svc.count() == 42


class TestSearch:
    def test_returns_flat_list(self):
        result = _chroma_result(
            ids=["p1", "p2"],
            docs=["doc1", "doc2"],
            metas=[{"name": "A"}, {"name": "B"}],
            distances=[0.1, 0.3],
        )
        svc = _make_service(query_result=result)
        items = svc.search("who has criminal cases", n_results=2)
        assert len(items) == 2
        assert items[0]["id"] == "p1"
        assert items[0]["document"] == "doc1"
        assert items[0]["distance"] == 0.1
        assert items[1]["id"] == "p2"

    def test_passes_type_filter(self):
        svc = _make_service(query_result=_chroma_result([], [], [], []))
        svc.search("q", politician_type="MP")
        call_kwargs = svc.vdb.query.call_args.kwargs
        assert call_kwargs["where"] == {"type": "MP"}

    def test_passes_state_filter(self):
        svc = _make_service(query_result=_chroma_result([], [], [], []))
        svc.search("q", state="Kerala")
        call_kwargs = svc.vdb.query.call_args.kwargs
        assert call_kwargs["where"] == {"state": "Kerala"}

    def test_no_filter_passes_none(self):
        svc = _make_service(query_result=_chroma_result([], [], [], []))
        svc.search("q")
        call_kwargs = svc.vdb.query.call_args.kwargs
        assert call_kwargs["where"] is None

    def test_returns_empty_list_when_no_ids(self):
        svc = _make_service(
            query_result={"ids": [], "documents": [], "metadatas": [], "distances": []}
        )
        items = svc.search("nothing")
        assert items == []

    def test_handles_none_result(self):
        svc = _make_service(query_result=None)
        items = svc.search("q")
        assert items == []
