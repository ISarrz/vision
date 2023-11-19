from style import *


if __name__ == '__main__':
    from classes import Application
    from settings_page import second_target

    from functions import *
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
        e.control.selected = not e.control.selected
        page.update()
        a = Application()
        a.generate_frames(e)



    def pause(e):
        if play_button.selected:
            if e.control.selected:
                play_button.content.controls[0].value = play_button.content.controls[0].value.replace('p', '')
                pause_button.selected = not pause_button.selected
            else:

                play_button.content.controls[0].value += 'p'
                pause_button.selected = not pause_button.selected
            e.control.update()
    def screen(e):
        if play_button.selected:
            play_button.content.controls[0].value += 's'

    def convert(e):
        if play_button.selected:
            play_button.content.controls[0].value += 'c'
        while 'c' in play_button.content.controls[0].value:
            pass
        text_widget.value = play_button.content.controls[1].value
        text_widget.update()
    def close(e):
        page.window_close()
        exit()

    text_widget = TextField(expand=True, value='Test', color=colors.WHITE, multiline=True,
                            border_color=colors.TRANSPARENT)

    def refresh(e):
        text_widget.value = ''
        text_widget.update()

    def close_dlg_ok(e):
        dlg_modal_ok.open = False
        page.update()

    def open_dlg_ok():
        page.dialog = dlg_modal_ok
        dlg_modal_ok.open = True
        page.update()

    def close_dlg_error(e):
        dlg_modal_error.open = False
        page.update()

    def open_dlg_error():
        page.dialog = dlg_modal_error
        dlg_modal_error.open = True
        page.update()

    dlg_modal_ok = AlertDialog(
        modal=True,

        actions=[
            Container(
                padding=5,
                alignment=alignment.center,
                content=
                Column([
                    Text('Saved', scale=2),

                    TextButton('OK', on_click=close_dlg_ok)
                ],
                    horizontal_alignment=CrossAxisAlignment.CENTER)
            )

        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    dlg_modal_error = AlertDialog(
        modal=True,

        actions=[
            Container(
                padding=5,
                alignment=alignment.center,
                content=
                Column([
                    Text('Error', scale=2),

                    TextButton('OK', on_click=close_dlg_error)
                ],
                    horizontal_alignment=CrossAxisAlignment.CENTER)
            )

        ],
        actions_alignment=MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def pick_files_result(e: FilePickerResultEvent):
        s = e.path
        if s:
            text = text_widget.value
            try:
                with open(s, 'w') as file:
                    file.write(text)
                open_dlg_ok()
            except Exception:
                open_dlg_error()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    page.overlay.append(pick_files_dialog)

    play_button = IconButton(
        top=-5,
        icon=icons.PLAY_ARROW_ROUNDED,
        selected_icon=icons.STOP_ROUNDED,
        on_click=play,
        style=buttons_style,
        content=Row([Text(''), Text('')])
    )
    pause_button = IconButton(
        top=-5,
        left=30,
        icon=icons.PAUSE_ROUNDED,
        selected_icon=icons.PLAY_ARROW_ROUNDED,
        on_click=pause,
        style=buttons_style,

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
                on_click=close  ,
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
                        play_button,
                        pause_button,


                        IconButton(
                            top=-5,
                            left=60,
                            icon=icons.CAMERA,
                            on_click=screen,
                            style=buttons_style
                        ),

                        IconButton(
                            top=-5,
                            left=90,
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
                            on_click=lambda _: pick_files_dialog.save_file(),
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
