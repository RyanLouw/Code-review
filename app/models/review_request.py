from pydantic import BaseModel, Field


class BuildRequest(BaseModel):
    project_path: str = Field(min_length=1, description="Path to the .NET project or solution")
    run_tests: bool = True


class CommandResult(BaseModel):
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str


class BuildResponse(BaseModel):
    success: bool
    restore: CommandResult
    build: CommandResult | None = None
    test: CommandResult | None = None
