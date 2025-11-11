import typing as t


class GoogleDriveImageIdsDataParser:
    def parse(self, data: t.Dict[t.Any, t.Any]) -> t.List[str]:
        return [obj_data["id"] for obj_data in data["files"] if obj_data["mimeType"] != "folder"]
