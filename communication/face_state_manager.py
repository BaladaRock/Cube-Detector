from __future__ import annotations
import json, os, tempfile
from pathlib import Path
from typing import List

# default configuration
FACES = ["F", "B", "U", "R", "L", "D"]
CUBE_DIR  = Path(__file__).parent
CUBE_FILE = CUBE_DIR / "cube_state.json"
CUBE_DIR.mkdir(parents=True, exist_ok=True)

def _default_state() -> dict:
    return {f: [["white"] * 3 for _ in range(3)] for f in FACES}

def _load_state() -> dict:
    if not CUBE_FILE.exists():
        return _default_state()
    try:
        with CUBE_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError):
        return _default_state()

def _atomic_write(state: dict) -> None:
    lines = []
    for face in FACES:
        grid = state.get(face, [["white"] * 3 for _ in range(3)])
        grid_str = json.dumps(grid, ensure_ascii=False, separators=(',', ':'))
        lines.append(f'  "{face}":{grid_str}')

    content = "{\n" + ",\n".join(lines) + "\n}"

    with tempfile.NamedTemporaryFile("w",
                                     dir=CUBE_DIR,
                                     delete=False,
                                     encoding="utf-8") as tmp:
        tmp.write(content)
        tmp.flush()
        os.fsync(tmp.fileno())
    Path(tmp.name).replace(CUBE_FILE)

def _normalize_grid(grid: List[List[str]]) -> List[List[str]]:
    return [[cell if cell else "white" for cell in row] for row in grid]

# Public API
def update_face(face_id: str, grid: List[List[str]]) -> None:
    face_id = face_id.upper()
    if face_id not in FACES:
        raise ValueError(f"face_id must be one of the valid faces {FACES}, not {face_id!r}")

    state = _load_state()
    state[face_id] = _normalize_grid(grid)
    _atomic_write(state)

def get_state() -> dict:
    return _load_state()

if not CUBE_FILE.exists():
    _atomic_write(_default_state())
