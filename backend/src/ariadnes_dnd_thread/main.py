from fastapi import FastAPI

app = FastAPI(title="Ariadne's Dnd Thread")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: the process is up. Does not touch the database."""
    return {"status": "ok"}
