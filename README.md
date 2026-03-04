# Document Intelligence Refinery

This repo implements the TRP1 Week 3 pipeline: triage agent, multi-strategy extraction, semantic chunking, PageIndex builder, and query agent with provenance.

## Quick start

```bash
pip install -e .
python -c "from pathlib import Path; from src.agents.triage import TriageAgent; from src.agents.extractor import ExtractionRouter; from src.agents.chunker import ChunkingEngine; from src.agents.indexer import PageIndexBuilder; from src.agents.query_agent import QueryAgent; triage=TriageAgent(); router=ExtractionRouter(); ce=ChunkingEngine(); pib=PageIndexBuilder(); pdf=Path('data/sample.pdf'); profile=triage.profile_document(pdf); doc=router.extract(pdf, profile); ldus=ce.chunk(doc); index=pib.build(profile.doc_id, ldus); agent=QueryAgent(ldus, index); print(agent.answer('What is this document about?'))"
```
