from pic_back.routers.shared.serializers.output import ResponseMessage


def test_fields():
    msg = "Something something"

    response_msg = ResponseMessage(detail=msg)

    assert response_msg.detail == msg
