# -*- coding: utf-8 -*-

import time

import asyncio
import blivedm


class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        print(command)
    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter  # 老爷入场

    async def _on_receive_popularity(self, popularity: int):
        t = time.time()
        print(f'{t}: 当前人气值：{popularity}')

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        t = time.time()
        print(f'{t}: {danmaku.uname}：{danmaku.msg}')

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        t = time.time()
        print(f'{t}: {gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        t = time.time()
        print(f'{t}: {message.username} 购买{message.gift_name}')


async def main():
    # 139是黑桐谷歌的直播间
    # 如果SSL验证失败就把第二个参数设为False
    client = MyBLiveClient(383045, True)
    future = client.start()
    try:
        # 5秒后停止，测试用
        # await asyncio.sleep(5)
        # future = client.stop()
        # 或者
        # future.cancel()

        await future
    finally:
        await client.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
