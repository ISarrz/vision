from flet_multi_page import subPage
from flet import *
import cv2
import json
from settings_page import second_target

DG = "#1C1F22"
BG = "#23272a"
G = "#2c2f33"
LG = "#99aab5"


def resize_image(image, size):
    height, width = image.shape[:2]
    new_width, new_height = size
    otn = width / height
    if otn >= 1:
        if new_width < new_height:
            image = cv2.resize(image, (int(new_height * otn), new_height))
        else:
            image = cv2.resize(image, (new_width, int(new_width / otn)))
    else:
        if new_width > new_height:
            image = cv2.resize(image, (int(new_height * otn), new_height))
        else:
            image = cv2.resize(image, (new_width, int(new_width / otn)))
    return image


with open('data/settings.json', 'r') as file:
    settings_data = json.load(file)
buttons_style = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.WHITE,
        MaterialState.DEFAULT: LG,
    },
    overlay_color=colors.TRANSPARENT,
)
buttons_style_red = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.RED,
        MaterialState.DEFAULT: LG,
    },
    overlay_color=colors.TRANSPARENT,
)
buttons_style_light_red = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.RED,
        MaterialState.DEFAULT: DG,
    },
    overlay_color=colors.TRANSPARENT,
)
buttons_style_light_green = ButtonStyle(
    color={
        MaterialState.HOVERED: colors.GREEN,
        MaterialState.DEFAULT: DG,
    },
    overlay_color=colors.TRANSPARENT,
)


def main(page: Page):
    page.bgcolor = G
    page.window_height = 800
    page.window_width = 800
    page.padding = 0
    page.window_title_bar_hidden = True
    page.window_center()

    def minimize(e):
        page.window_minimized = True
        page.update()

    def full_screen(e):
        e.control.selected = not e.control.selected
        page.window_full_screen = not page.window_full_screen
        page.update()

    def settings(e):
        p = subPage(target=second_target)  # ! This is the "subPage" class.
        p.start()  # ! This will run and start the second page.

    def play(e):
        width = int(settings_data['video_window_size'][0])
        height = int(settings_data['video_window_size'][1])

        if not e.control.selected:
            e.control.selected = True
            e.control.update()
            camera = cv2.VideoCapture('3.mp4')
            while True and e.control.selected:
                res, frame = camera.read()
                if not res:
                    break
                frame = resize_image(frame, (width, height))
                cv2.imshow('Video', frame)
                cv2.moveWindow("Video", 500, 500)
                # cv2.resizeWindow()
                cv2.waitKey(2)

            cv2.destroyAllWindows()
            camera.release()
            e.control.selected = False
            e.control.update()
        else:
            e.control.selected = False
            e.control.update()

    def screen(e):
        pass

    def convert(e):
        pass

    text_widget = TextField(expand=True, value='Test', color=colors.WHITE, multiline=True,
                            border_color=colors.TRANSPARENT)

    def refresh(e):
        text_widget.value = ''
        text_widget.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    def open_dlg():
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def save(e):
        open_dlg()

    def save_file(e):
        s = dlg_modal.actions[0].content.controls[1].value
        text = text_widget.value
        with open(s, 'w') as file:
            file.write(text)
        close_dlg(e)

    dlg_modal = AlertDialog(
        modal=True,

        actions=[
            Container(
                padding=5,
                alignment=alignment.center,
                content=
                Column([
                    Text('Saving', scale=2),
                    TextField(label='Enter filename'),
                    Row([
                        TextButton("Save", on_click=save_file, style=buttons_style_light_green, scale=1.5),
                        TextButton("Cancel", on_click=close_dlg, style=buttons_style_light_red, scale=1.5)
                    ],
                        alignment=MainAxisAlignment.CENTER
                    )
                ],
                    horizontal_alignment=CrossAxisAlignment.CENTER)
            )

        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    menu_bar = Container(
        animate_opacity=100,
        opacity=0,
        disabled=True,
        visible=True,
        left=40,
        padding=0,
        content=
        Row([
            IconButton(
                icon=icons.SETTINGS,
                selected_icon=icons.SETTINGS,
                on_click=settings,
                style=buttons_style
            )
        ])
    )

    def menu(e):
        e.control.selected = not e.control.selected
        menu_bar.disabled = not menu_bar.disabled
        menu_bar.opacity = 0 if menu_bar.opacity else 1
        top.update()

    top = Container(
        border=border.only(bottom=border.BorderSide(1, DG)),
        content=
        Stack([
            Row([WindowDragArea(Container(Text(), bgcolor=BG, padding=10), expand=True), ]),
            menu_bar,
            IconButton(
                icon=icons.MENU_ROUNDED,
                selected_icon=icons.MENU_OPEN_ROUNDED,
                on_click=menu,
                left=5,
                style=buttons_style
            ),

            IconButton(
                icon=icons.FULLSCREEN_ROUNDED,
                selected_icon=icons.FULLSCREEN_EXIT_ROUNDED,
                on_click=full_screen,
                right=30,
                style=buttons_style
            ),

            IconButton(
                icon=icons.MINIMIZE_SHARP,
                on_click=minimize,
                right=60,
                top=-8,
                style=buttons_style
            ),

            IconButton(
                icon=icons.CLOSE,
                on_click=lambda _: page.window_close(),
                right=0,
                style=buttons_style_red
            )

        ])
    )

    workspace = Container(
        expand=True,
        alignment=alignment.center,
        bgcolor=colors.TRANSPARENT,
        padding=10,
        content=
        Column(
            expand=True,
            controls=[
                Container(
                    expand=False,
                    height=30,
                    border_radius=10, bgcolor=BG,
                    border=border.all(1, DG),
                    content=
                    Stack([
                        Row([Text()], expand=True),
                        IconButton(
                            top=-5,
                            icon=icons.PLAY_ARROW_ROUNDED,
                            selected_icon=icons.STOP_ROUNDED,
                            on_click=play,
                            style=buttons_style
                        ),

                        IconButton(
                            top=-5,
                            left=30,
                            icon=icons.CAMERA,
                            on_click=screen,
                            style=buttons_style
                        ),

                        IconButton(
                            top=-5,
                            left=60,
                            icon=icons.REMOVE_RED_EYE_OUTLINED,
                            on_click=convert,
                            style=buttons_style
                        ),

                    ])

                ),
                Container(
                    padding=5,
                    # alignment=alignment.top_left,
                    expand=True,
                    border_radius=10,
                    bgcolor=BG,
                    border=border.all(1, DG),
                    content=text_widget
                ),

                Container(
                    expand=False,
                    height=30,
                    border_radius=10, bgcolor=BG,
                    border=border.all(1, DG),
                    content=Stack([
                        IconButton(
                            icon=icons.REFRESH_ROUNDED,
                            on_click=refresh,
                            top=-5,
                            left=0,
                            style=buttons_style
                        ),
                        IconButton(
                            icon=icons.SAVE,
                            on_click=save,
                            left=30,
                            top=-5,
                            style=buttons_style
                        ),

                    ]))

            ])
    )

    inter = Column([top, workspace], expand=True)
    page.add(inter)


if __name__ == "__main__":  # ? This is so important, there will be errors without it.
    app(target=main)
