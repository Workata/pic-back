import typing as t


class GoogleDriveImageIdsDataParser:
    def parse(self, data: t.Dict[t.Any, t.Any]) -> t.List[str]:
        return [img_data['id'] for img_data in data['files']]
