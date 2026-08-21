from fastapi import FastAPI

from app.api.review_routes import router as review_router

app = FastAPI(
    title="Code Review Runner",
    version="0.1.0",
    description="Local CI-style build and test runner for code review workflows.",
)

app.include_router(review_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
