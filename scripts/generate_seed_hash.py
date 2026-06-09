#!/usr/bin/env python3
"""Generate bcrypt hash for demo seed password (123456). Run from backend: python ../scripts/generate_seed_hash.py"""
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(backend_dir))


def generate_hash(password: str = "123456") -> str:
    try:
        from core.seguranca import hash_senha

        return hash_senha(password)
    except Exception:
        import bcrypt

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


if __name__ == "__main__":
    print(generate_hash())
