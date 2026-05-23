import json
from pathlib import Path


def test_root_package_scripts_delegate_to_frontend_package() -> None:
    package = json.loads(Path("package.json").read_text(encoding="utf-8"))

    assert package["private"] is True
    assert package["scripts"]["install:frontend"] == "npm --prefix frontend install"
    assert package["scripts"]["dev"] == "npm --prefix frontend run dev --"
    assert package["scripts"]["typecheck"] == "npm --prefix frontend run typecheck"
    assert package["scripts"]["build"] == "npm --prefix frontend run build"
    assert package["scripts"]["lint"] == "npm --prefix frontend run lint"


def test_root_package_does_not_own_frontend_dependencies() -> None:
    package = json.loads(Path("package.json").read_text(encoding="utf-8"))

    assert "dependencies" not in package
    assert "devDependencies" not in package
    assert Path("frontend/package.json").exists()
