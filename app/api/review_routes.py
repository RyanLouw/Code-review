from fastapi import APIRouter, HTTPException

from app.models.review_request import BuildRequest, BuildResponse
from app.services.build_service import BuildService

router = APIRouter(prefix="/api/review", tags=["review"])
build_service = BuildService()


@router.post("/build", response_model=BuildResponse)
async def build_project(request: BuildRequest) -> BuildResponse:
    try:
        return await build_service.run(request.project_path, request.run_tests)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Build runner failed: {exc}") from exc
