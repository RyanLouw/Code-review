import asyncio
from pathlib import Path

from app.models.review_request import BuildResponse, CommandResult


class BuildService:
    async def run(self, project_path: str, run_tests: bool = True) -> BuildResponse:
        path = Path(project_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Project path does not exist: {path}")

        restore = await self._execute(["dotnet", "restore", str(path)])
        if restore.exit_code != 0:
            return BuildResponse(success=False, restore=restore)

        build = await self._execute(
            ["dotnet", "build", str(path), "--no-restore", "--configuration", "Release"]
        )
        if build.exit_code != 0:
            return BuildResponse(success=False, restore=restore, build=build)

        test = None
        if run_tests:
            test = await self._execute(
                ["dotnet", "test", str(path), "--no-build", "--configuration", "Release"]
            )
            if test.exit_code != 0:
                return BuildResponse(
                    success=False,
                    restore=restore,
                    build=build,
                    test=test,
                )

        return BuildResponse(success=True, restore=restore, build=build, test=test)

    async def _execute(self, command: list[str]) -> CommandResult:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()

        return CommandResult(
            command=command,
            exit_code=process.returncode,
            stdout=stdout.decode(errors="replace"),
            stderr=stderr.decode(errors="replace"),
        )
