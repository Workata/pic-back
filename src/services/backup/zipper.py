import shutil


class Zipper:
    def zip(self, directory_path: str, output_file_path: str) -> None:
        output_file_path = output_file_path.replace(".zip", "")  # '.zip' extension added automatically via shutil
        shutil.make_archive(output_file_path, "zip", directory_path)
