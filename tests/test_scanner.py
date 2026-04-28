import os
import pytest
from filesizer.scanner import scan_directory


def make_file(path, size):
    path.write_bytes(b"x" * size)


class TestFlatDirectory:
    def test_sizes_correct(self, tmp_path):
        make_file(tmp_path / "a.txt", 100)
        make_file(tmp_path / "b.txt", 200)
        make_file(tmp_path / "c.txt", 300)

        result = scan_directory(str(tmp_path))

        assert result["is_dir"] is True
        assert result["size"] == 600
        assert len(result["children"]) == 3
        assert {c["name"] for c in result["children"]} == {"a.txt", "b.txt", "c.txt"}

    def test_file_node_structure(self, tmp_path):
        make_file(tmp_path / "test.txt", 42)
        result = scan_directory(str(tmp_path))
        node = next(c for c in result["children"] if c["name"] == "test.txt")
        assert node["is_dir"] is False
        assert node["children"] == []
        assert node["size"] == 42
        assert node["truncated"] is False


class TestNestedDirectories:
    def test_nested_size_rollup(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        make_file(sub / "inner.txt", 500)
        make_file(tmp_path / "outer.txt", 100)

        result = scan_directory(str(tmp_path))

        assert result["size"] == 600
        sub_node = next(c for c in result["children"] if c["name"] == "sub")
        assert sub_node["is_dir"] is True
        assert sub_node["size"] == 500

    def test_directory_node_children(self, tmp_path):
        sub = tmp_path / "mydir"
        sub.mkdir()
        make_file(sub / "f.txt", 10)

        result = scan_directory(str(tmp_path))
        dir_node = next(c for c in result["children"] if c["name"] == "mydir")
        assert len(dir_node["children"]) == 1
        assert dir_node["children"][0]["name"] == "f.txt"


class TestDepthLimit:
    def test_depth_limit_truncates(self, tmp_path):
        sub = tmp_path / "level1"
        sub.mkdir()
        deep = sub / "level2"
        deep.mkdir()
        make_file(deep / "deep.txt", 100)

        result = scan_directory(str(tmp_path), max_depth=1)

        sub_node = next(c for c in result["children"] if c["name"] == "level1")
        assert sub_node["truncated"] is True
        assert sub_node["children"] == []

    def test_no_depth_limit(self, tmp_path):
        sub = tmp_path / "a" / "b"
        sub.mkdir(parents=True)
        make_file(sub / "deep.txt", 1)

        result = scan_directory(str(tmp_path))

        def check(node):
            assert node["truncated"] is False
            for c in node["children"]:
                check(c)

        check(result)


class TestPermissionError:
    @pytest.mark.skipif(os.name == "nt", reason="chmod not reliable on Windows")
    def test_permission_denied_skipped(self, tmp_path):
        locked = tmp_path / "locked"
        locked.mkdir()
        make_file(locked / "secret.txt", 100)
        locked.chmod(0o000)
        try:
            result = scan_directory(str(tmp_path))
            assert result["is_dir"] is True
        finally:
            locked.chmod(0o755)


class TestCycleDetection:
    @pytest.mark.skipif(os.name == "nt", reason="Symlink creation requires elevation on Windows")
    def test_symlink_cycle_completes(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "back").symlink_to(tmp_path)

        result = scan_directory(str(tmp_path))
        assert result["is_dir"] is True