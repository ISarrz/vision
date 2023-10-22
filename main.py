from flet import *
import cv2
import asyncio


class Countdown(Image):
    def __init__(self):
        super().__init__()
        print('init')

    async def did_mount_async(self):
        print('did')
        self.running = True
        asyncio.create_task(self.update_timer())

    async def will_unmount_async(self):
        print('will')
        self.running = False

    async def update_timer(self):
        camera = cv2.VideoCapture('3.mp4')
        while True:
            res, frame = camera.read()
            if not res:
                break
            cv2.imwrite('work.jpeg', frame)
            self.src = 'work.jpeg'
            await self.update_async()
            await asyncio.sleep(1)

            print('update')



    def build(self):
        print('build')
        self.image = Image(
            src=f"",
            width=100,
            height=100,
            fit=ImageFit.CONTAIN,
            border_radius=border_radius.all(10)
        )
        return self.countdown

async def main(page: Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    def minimize():
        page.window_minimized = True

    BG = "#23272a"
    G = "#2c2f33"
    LG = "#99aab5"
    page.bgcolor = BG

    page.window_height = 800
    page.window_width = 1500
    page.padding = 0
    page.window_title_bar_hidden = True
    page.window_center()

    def minimize(e):
        page.window_minimized = True
        page.update()

    def full_screen(e):
        e.control.selected = not e.control.selected
        if page.window_full_screen:

            page.window_full_screen = False
        else:

            page.window_full_screen = True
        page.update()

    def settings(e):
        pass

    frame = cv2.imread('test.jpeg')
    cv2.imwrite('work.jpeg', frame)

    img = Image(
        src='work.jpeg',
        width=1000,
        height=800,
        fit=ImageFit.CONTAIN,

        
    )
    menu_bar = Container(
        animate_opacity=100,

        opacity=0,
        disabled=True,
        visible=True,
        left=40,
        content=Row([
            IconButton(icon=icons.SETTINGS, selected_icon=icons.SETTINGS, on_click=settings,

                       style=ButtonStyle(
                           color={
                               MaterialState.HOVERED: colors.WHITE,
                               MaterialState.DEFAULT: LG,
                           },
                           overlay_color=colors.TRANSPARENT,
                       )
                       )
        ])
    )

    def menu(e):
        e.control.selected = not e.control.selected
        menu_bar.disabled = not menu_bar.disabled

        menu_bar.opacity = 0 if menu_bar.opacity else 1


        top.update()

    top = Stack([
        Row(
            [
                WindowDragArea(
                    Container(Text(),
                              bgcolor=G, padding=10), expand=True),

            ]
        ),
        IconButton(icon=icons.MENU_ROUNDED, selected_icon=icons.MENU_OPEN_ROUNDED, on_click=menu,
                   left=5,
                   style=ButtonStyle(
                       color={
                           MaterialState.HOVERED: colors.WHITE,
                           MaterialState.DEFAULT: LG,
                       },
                       overlay_color=colors.TRANSPARENT,
                   )
                   ),
        menu_bar,
        IconButton(icon=icons.FULLSCREEN_ROUNDED, selected_icon=icons.FULLSCREEN_EXIT_ROUNDED, on_click=full_screen,
                   right=30,
                   style=ButtonStyle(
                       color={
                           MaterialState.HOVERED: colors.WHITE,
                           MaterialState.DEFAULT: LG,
                       },
                       overlay_color=colors.TRANSPARENT,
                   )
                   ),
        IconButton(icons.MINIMIZE_SHARP, on_click=minimize, right=60, top=-8,
                   style=ButtonStyle(
                       color={
                           MaterialState.HOVERED: colors.WHITE,
                           MaterialState.DEFAULT: LG,
                       },
                       overlay_color=colors.TRANSPARENT,
                   )
                   ),
        IconButton(icons.CLOSE, on_click=lambda _: page.window_close(), right=0,
                   style=ButtonStyle(
                       color={
                           MaterialState.HOVERED: colors.RED,
                           MaterialState.DEFAULT: LG,
                       },
                       overlay_color=colors.TRANSPARENT,
                   )
                   )

    ])
    page.add(top, img)


app(target=main, assets_dir="assets")
