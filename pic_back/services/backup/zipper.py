import shutil
from pathlib import Path


class Zipper:
    def zip(self, directory_path: Path, output_file_path: Path) -> None:
        """
        '.zip' extension added automatically via shutil
        """
        shutil.make_archive(base_name=str(output_file_path.with_suffix("")), format="zip", root_dir=str(directory_path))
