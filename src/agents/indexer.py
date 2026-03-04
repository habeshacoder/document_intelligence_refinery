from typing import List
from collections import defaultdict

from src.models.ldu import LDU
from src.models.pageindex import PageIndexNode


class PageIndexBuilder:
    def __init__(self, summarize_fn=None):
        # summarize_fn(text) -> short summary; inject your LLM call here
        self.summarize_fn = summarize_fn or (lambda text: text[:200])

    def build(self, doc_id: str, ldus: List[LDU]) -> PageIndexNode:
        # simple grouping by page: one child node per page
        by_page: dict[int, List[LDU]] = defaultdict(list)
        for l in ldus:
            for p in l.page_refs:
                by_page[p].append(l)

        pages = sorted(by_page.keys())
        children: List[PageIndexNode] = []

        for p in pages:
            page_ldus = by_page[p]
            concat = "\n".join(l.content[:500] for l in page_ldus)
            summary = self.summarize_fn(concat)
            node = PageIndexNode(
                title=f"Page {p}",
                page_start=p,
                page_end=p,
                key_entities=[],  # TODO: add NER
                summary=summary,
                data_types_present=list({l.chunk_type for l in page_ldus}),
                children=[],
            )
            children.append(node)

        root_summary = f"{doc_id} with {len(ldus)} chunks and {len(pages)} pages."
        root = PageIndexNode(
            title=doc_id,
            page_start=pages[0] if pages else 1,
            page_end=pages[-1] if pages else 1,
            key_entities=[],
            summary=root_summary,
            data_types_present=list(
                {t for n in children for t in n.data_types_present}
            ),
            children=children,
        )
        return root
