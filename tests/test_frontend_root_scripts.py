import json
import re
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


def test_vite_proxy_covers_frontend_api_prefixes() -> None:
    runtime_client = Path("frontend/src/api/runtime.ts").read_text(
        encoding="utf-8"
    )
    vite_config = Path("frontend/vite.config.ts").read_text(encoding="utf-8")
    api_prefixes = {
        match.group(1)
        for match in re.finditer(r'fetch\("(/[^"/?]+)', runtime_client)
    }

    for prefix in sorted(api_prefixes):
        assert f'"{prefix}"' in vite_config, (
            f"frontend API prefix {prefix} must be proxied by Vite"
        )
