from .base_output_serializer import BaseOutputSerializer


class ResponseMessage(BaseOutputSerializer):
    detail: str
