import typing as t


class GoogleDriveImageIdsDataParser:
    def parse(self, data: t.Dict[t.Any, t.Any]) -> t.List[str]:
        content_objects = data["files"]
        image_ids = []
        for obj in content_objects:
            if "folder" in obj.pop("mimeType"):
                continue
            image_ids.append(obj["id"])
        return image_ids
