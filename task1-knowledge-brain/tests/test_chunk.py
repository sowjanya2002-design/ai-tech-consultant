from retrieval.store import chunk

def test_chunking_overlap():
    text = "A" * 2500
    chunks = chunk(text, size=1000, overlap=200)
    assert len(chunks) == 3
    assert len(chunks[0]) == 1000
    assert chunks[0][-200:] == chunks[1][:200]
