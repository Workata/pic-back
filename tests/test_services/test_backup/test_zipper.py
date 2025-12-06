from pathlib import Path

from pic_back.services.backup.zipper import Zipper


def test_zipper(tmp_path):
    zipper = Zipper()
    directory_to_zip = Path(tmp_path, "dir")
    directory_to_zip.mkdir()
    output_file_path = Path(tmp_path, "file.zip")

    zipper.zip(directory_to_zip, output_file_path)

    assert output_file_path.exists()
