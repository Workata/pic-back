from pic_back.routers.shared.serializers.output import BaseOutputSerializer


class TokenOutputSerializer(BaseOutputSerializer):
    access_token: str
    token_type: str = "bearer"
