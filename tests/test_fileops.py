import pytest
from filesizer.fileops import ConflictError, PathError, delete_item, move_item, validate_path


class TestValidatePath:
    def test_valid_path_inside_root(self, tmp_path):
        sub = tmp_path / "subdir"
        sub.mkdir()
        result = validate_path(str(sub), str(tmp_path))
        assert result is not None

    def test_path_equals_root_allowed(self, tmp_path):
        result = validate_path(str(tmp_path), str(tmp_path))
        assert result is not None

    def test_path_outside_root_raises(self, tmp_path):
        with pytest.raises(PathError):
            validate_path(str(tmp_path.parent), str(tmp_path))

    def test_path_traversal_blocked(self, tmp_path):
        evil = str(tmp_path) + "/subdir/../../etc/passwd"
        with pytest.raises(PathError):
            validate_path(evil, str(tmp_path))


class TestDeleteItem:
    def test_missing_path_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            delete_item(str(tmp_path / "nope.txt"), str(tmp_path))

    def test_outside_root_raises(self, tmp_path):
        with pytest.raises(PathError):
            delete_item(str(tmp_path.parent), str(tmp_path))

    def test_permanent_delete_file(self, tmp_path):
        f = tmp_path / "del.txt"
        f.write_bytes(b"hello")
        delete_item(str(f), str(tmp_path), permanent=True)
        assert not f.exists()

    def test_permanent_delete_directory(self, tmp_path):
        d = tmp_path / "deletedir"
        d.mkdir()
        (d / "file.txt").write_bytes(b"x")
        delete_item(str(d), str(tmp_path), permanent=True)
        assert not d.exists()


class TestMoveItem:
    def test_move_file_into_directory(self, tmp_path):
        src = tmp_path / "source.txt"
        src.write_bytes(b"data")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()

        move_item(str(src), str(dst_dir), str(tmp_path))

        assert not src.exists()
        assert (dst_dir / "source.txt").exists()

    def test_missing_source_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            move_item(str(tmp_path / "nope.txt"), str(tmp_path), str(tmp_path))

    def test_conflict_raises(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_bytes(b"a")
        dst_dir = tmp_path / "dest"
        dst_dir.mkdir()
        (dst_dir / "file.txt").write_bytes(b"b")

        with pytest.raises(ConflictError):
            move_item(str(src), str(dst_dir), str(tmp_path))

    def test_destination_outside_root_raises(self, tmp_path):
        src = tmp_path / "file.txt"
        src.write_bytes(b"x")
        with pytest.raises(PathError):
            move_item(str(src), str(tmp_path.parent), str(tmp_path))