from pathlib import Path

from src.agents.triage import TriageAgent
from src.agents.extractor import ExtractionRouter
from src.agents.chunker import ChunkingEngine
from src.agents.indexer import PageIndexBuilder
from src.agents.query_agent import QueryAgent

pdf = Path("data/sample.pdf")

triage = TriageAgent()
router = ExtractionRouter()
chunker = ChunkingEngine()
indexer = PageIndexBuilder()

profile = triage.profile_document(pdf)
print("PROFILE:", profile)

doc = router.extract(pdf, profile)
print("Extracted blocks:", len(doc.text_blocks))

ldus = chunker.chunk(doc)
print("LDUs:", len(ldus))

index = indexer.build(profile.doc_id, ldus)

agent = QueryAgent(ldus, index)
answer, prov = agent.answer("What is this document about?")
print("ANSWER:", answer)
print("PROVENANCE:", prov)
