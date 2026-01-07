from pic_back.routers.shared.serializers.output import BaseOutputSerializer


class GoogleDriveFolderOutputSerializer(BaseOutputSerializer):
    id: str
    name: str
