import asyncio
import flet as ft


class Countdown(ft.UserControl):
    def __init__(self, seconds):
        super().__init__()
        self.seconds = seconds
        print('init')

    async def did_mount_async(self):
        print('did')
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self):
        print('will')
        self.running = False

    async def update_timer(self):
        colors = [ft.colors.WHITE, ft.colors.BLACK, ft.colors.YELLOW, ft.colors.GREEN, ft.colors.RED]
        print('update')
        id = 0
        while True:
            self.countdown.bgcolor = colors[id]
            await self.update_async()
            await asyncio.sleep(2)
            id += 1
            id %= len(colors)


    def build(self):
        print('build')
        self.countdown = ft.Container(
            width=100,
            height=100,
            bgcolor=ft.colors.RED
        )
        return self.countdown


async def main(page: ft.Page):
    await page.add_async(Countdown(120))


ft.app(target=main)
