from nonebot import get_driver

from .config import Config

from nonebot import on_command
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11.message import MessageSegment

from . import ahs_tool

global_config = get_driver().config
config = Config(**global_config.dict())

matcher = on_command("tts", priority=5)
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


@matcher.handle()
async def handle_msg(event: Event):
    in_txt = str(event.get_message()).strip()
    audio = ahs_tool.ahs_audio_down(intxt=in_txt)
    audio.get_audio()
    await matcher.finish(MessageSegment.record(file=f'file://{audio.cut()}'))
