import pytest
from fastapi.testclient import TestClient

from filesizer.server import app

client = TestClient(app)


class TestScanEndpoint:
    def test_valid_scan(self, tmp_path):
        (tmp_path / "file.txt").write_bytes(b"hello")
        res = client.get("/api/scan", params={"path": str(tmp_path)})
        assert res.status_code == 200
        data = res.json()
        assert data["is_dir"] is True
        assert len(data["children"]) == 1
        assert data["children"][0]["name"] == "file.txt"

    def test_nonexistent_path_returns_400(self, tmp_path):
        res = client.get("/api/scan", params={"path": str(tmp_path / "nope")})
        assert res.status_code == 400

    def test_file_path_returns_400(self, tmp_path):
        f = tmp_path / "f.txt"
        f.write_bytes(b"x")
        res = client.get("/api/scan", params={"path": str(f)})
        assert res.status_code == 400

    def test_depth_param_truncates(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "deep.txt").write_bytes(b"x")
        res = client.get("/api/scan", params={"path": str(tmp_path), "depth": 1})
        assert res.status_code == 200
        sub_node = next(c for c in res.json()["children"] if c["name"] == "sub")
        assert sub_node["truncated"] is True


class TestDeleteEndpoint:
    def test_delete_file_permanent(self, tmp_path):
        f = tmp_path / "del.txt"
        f.write_bytes(b"x")
        res = client.post("/api/delete", json={
            "path": str(f), "root": str(tmp_path), "permanent": True
        })
        assert res.status_code == 200
        assert not f.exists()

    def test_delete_missing_returns_404(self, tmp_path):
        res = client.post("/api/delete", json={
            "path": str(tmp_path / "nope"), "root": str(tmp_path), "permanent": True
        })
        assert res.status_code == 404

    def test_delete_outside_root_returns_403(self, tmp_path):
        res = client.post("/api/delete", json={
            "path": str(tmp_path.parent), "root": str(tmp_path), "permanent": True
        })
        assert res.status_code == 403


class TestMoveEndpoint:
    def test_move_file(self, tmp_path):
        src = tmp_path / "src.txt"
        src.write_bytes(b"data")
        dst = tmp_path / "subdir"
        dst.mkdir()
        res = client.post("/api/move", json={
            "source": str(src), "destination": str(dst), "root": str(tmp_path)
        })
        assert res.status_code == 200
        assert not src.exists()
        assert (dst / "src.txt").exists()

    def test_move_conflict_returns_409(self, tmp_path):
        src = tmp_path / "f.txt"
        src.write_bytes(b"a")
        dst = tmp_path / "dest"
        dst.mkdir()
        (dst / "f.txt").write_bytes(b"b")
        res = client.post("/api/move", json={
            "source": str(src), "destination": str(dst), "root": str(tmp_path)
        })
        assert res.status_code == 409

    def test_move_outside_root_returns_403(self, tmp_path):
        src = tmp_path / "f.txt"
        src.write_bytes(b"x")
        res = client.post("/api/move", json={
            "source": str(src), "destination": str(tmp_path.parent), "root": str(tmp_path)
        })
        assert res.status_code == 403