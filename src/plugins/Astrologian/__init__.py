import random

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.log import logger
from . import utils

ffxiv_zhanbu = on_command('/占卜', aliases={'/zhanbu'})


# on_command 装饰器将函数声明为一个命令处理器
@ffxiv_zhanbu.handle()
async def luck(bot: Bot, event: Event, state: dict):
    if len(utils.war or utils.magic or utils.land or utils.hand or utils.stains) == 0:
        await utils.initialization()
    # 拿到命令使用者的qq号
    caller_qq_number = event.user_id
    logger.info(caller_qq_number)
    # 生成当天种子
    r = random.Random(await utils.get_seed(caller_qq_number))
    # content
    # 运势 1-100
    luck_number = str(r.randint(1, 100))
    # 职业 ff14全部职业
    luck_job = await utils.sub_event(str(r.choice(utils.war + utils.magic + utils.land + utils.hand)))
    # 宜
    luck_event = r.choice(utils.EVENT_LIST)
    # 忌
    unlucky_event = utils.EVENT_LIST.copy()
    unlucky_event.remove(luck_event)
    unlucky_event = r.choice(unlucky_event)
    # 染剂
    stain = r.choice(utils.stains)
    # 一言
    hint = await utils.get_hint(luck_number, luck_job, luck_event, unlucky_event, stain)

    message = "运势: " + luck_number + "%  幸运职业: " \
              + luck_job + "\n宜: " + luck_event + "  忌: " + unlucky_event + "  幸运染剂: " + stain + "\n" + hint
    # print(r.randint(0, len(EVENT_LIST) - 2))
    try:
        group_id = event.group_id
        await ffxiv_zhanbu.send("\n" + message, at_sender=True)
    except:
        await ffxiv_zhanbu.send(message)
