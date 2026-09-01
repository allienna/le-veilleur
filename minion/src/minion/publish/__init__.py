"""Publishing layer: the Imagen hero image and the GitHub commit that publishes the day.

Mirrors `ingest/` and `generate/`: the publish steps depend on the Protocols in `ports.py`,
the production adapters (`imagen.py`, `github.py`) implement them, and `fakes.py` provides
hermetic doubles so the whole pipeline runs without Vertex, GitHub, or network in CI.
"""
