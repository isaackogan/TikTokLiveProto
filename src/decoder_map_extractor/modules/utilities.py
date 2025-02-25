from typing import TypedDict

from antlr4 import ParserRuleContext

from antlr.generated.Java8Parser import Java8Parser


def extract_proto_decoder(text: str) -> str | None:
    """
    Extract the class responsible for proto decoding

    >>> extract_proto_decoder("bannerInfo.animationImage = _ImageModel_ProtoDecoder.LIZIZ(c140922mme);")
    '_ImageModel_ProtoDecoder.java'

    >>> extract_proto_decoder("bannerInfo.height = (int) c140922mme.LJIIJJI();")

    >>> extract_proto_decoder("bannerInfo.bannerList.add(_BannerInRoom_ProtoDecoder.LIZIZ(c140922mme));")
    '_BannerInRoom_ProtoDecoder.java'

    >>> extract_proto_decoder("_RoomNotifyMessageExtra_Background_ProtoDecoder.LIZIZ(c140922mme);")
    '_RoomNotifyMessageExtra_Background_ProtoDecoder.java'

    :param text: The java text to extract the proto decoder from
    :return: The extracted proto decoder

    """

    if '_ProtoDecoder' not in text:
        return None

    paths = text.split("_ProtoDecoder")[0].split("_")
    proto_name = "_".join(paths[1:])
    return f"_{proto_name}_ProtoDecoder.java"


class FieldMapping(TypedDict):
    field: int
    field_enum: str | None  # If it's a reference to an enum
    proto_decoder: str | None


def count_while_parents(ctx: ParserRuleContext) -> int:
    count = 0
    parent_ctx = ctx.parentCtx
    while parent_ctx is not None:
        if isinstance(parent_ctx, Java8Parser.WhileStatementContext):
            count += 1
        parent_ctx = parent_ctx.parentCtx
    return count


type FieldMap = dict[str, FieldMapping]
