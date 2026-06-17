from chunking import chunk_transcript


def test_chunking():

    sample = "Python " * 10000

    chunks = chunk_transcript(sample)

    print(f"Chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks, start=1):
        print(
            f"Chunk {i}: "
            f"{len(chunk.split())} words"
        )


if __name__ == "__main__":
    test_chunking()