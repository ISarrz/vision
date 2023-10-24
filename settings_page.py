from style import *
import cv2



def second_target(page: Page):
    page.bgcolor = G
    page.window_height = 800
    page.window_width = 800
    page.padding = 0
    page.window_title_bar_hidden = True
    page.window_center()

    def pick_files_result(e: FilePickerResultEvent):
        selected_files.value = e.files[0].path
        if selected_files.value:
            video_settings_widget.content.controls[1].controls[2].value = selected_files.value
            video_settings_widget.content.controls[1].controls[2].update()
            change_save_button(e)

    def change_save_button(e):
        top.content.controls[1].selected = False
        top.content.controls[1].update()

    pick_files_dialog = FilePicker(on_result=pick_files_result)
    selected_files = Text()
    page.overlay.append(pick_files_dialog)

    def minimize(e):
        page.window_minimized = True
        page.update()

    def full_screen(e):
        e.control.selected = not e.control.selected
        page.window_full_screen = not page.window_full_screen
        page.update()

    def save(e):
        if e.control.selected:
            return
        e.control.selected = True
        settings_data['video_file_name'] = video_settings_widget.content.controls[1].controls[2].value
        size = (video_settings_widget.content.controls[0].controls[1].controls[1].value,
                video_settings_widget.content.controls[0].controls[2].controls[1].value)
        settings_data['video_window_size'] = size
        input_type_bool = video_settings_widget.content.controls[1].controls[3].value
        if input_type_bool:
            settings_data['video_input_type'] = 'file'
        else:
            settings_data['video_input_type'] = 'stream'
        settings_data['video_input_name'] = video_settings_widget.content.controls[2].controls[2].text
        settings_data['video_type'] = video_settings_widget.content.controls[3].controls[1].value
        with open('data/settings.json', 'w') as file:
            json.dump(settings_data, file)
        e.control.update()

    def input_type(e):
        if e.control.label == '1':
            if e.control.value:
                video_settings_widget.content.controls[2].controls[4].value = False
            else:
                video_settings_widget.content.controls[2].controls[4].value = True
        else:
            if e.control.value:
                video_settings_widget.content.controls[1].controls[3].value = False
            else:
                video_settings_widget.content.controls[1].controls[3].value = True
        change_save_button(e)
        page.update()

    def input_name_update(e):
        if e.control.icon == icons.ARROW_LEFT:
            n = video_settings_widget.content.controls[2].controls[2].text
            if n == '0':
                return
            n = str(int(n) - 1)
            video_settings_widget.content.controls[2].controls[2].text = n
        else:
            n = video_settings_widget.content.controls[2].controls[2].text
            n = str(int(n) + 1)
            video_settings_widget.content.controls[2].controls[2].text = n
        page.update()
        change_save_button(e)

    top = Container(
        border=border.only(bottom=border.BorderSide(1, DG)),
        content=
        Stack([
            Row([WindowDragArea(Container(Text(), bgcolor=BG, padding=10), expand=True), ]),
            IconButton(
                icon=icons.SAVE,
                selected_icon=icons.DONE,
                on_click=save,
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

    video_settings_widget = Container(
        expand=8,
        padding=5,
        border_radius=10,
        bgcolor=BG,
        content=
        Column([
            Row([
                Text('Video window size', size=18, color=colors.WHITE),
                Column([
                    Text('width', size=18, color=colors.WHITE),
                    TextField(value=settings_data['video_window_size'][0], height=30, width=80, multiline=False,
                              text_align="CENTER", text_size=15, on_change=change_save_button, color=colors.WHITE)
                ],
                    spacing=0),
                Column([
                    Text('height', size=18, color=colors.WHITE),
                    TextField(value=settings_data['video_window_size'][1], height=30, width=80, multiline=False,
                              text_align="CENTER", text_size=15, on_change=change_save_button, color=colors.WHITE)
                ],
                    spacing=0),
            ]),
            Row([
                Text('Video file', size=18, color=colors.WHITE),

                IconButton(
                    icon=icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=True
                    ), style=ButtonStyle(color=colors.WHITE)

                ),
                TextField(value=settings_data['video_file_name'], height=90, width=300, multiline=True, text_align="CENTER",
                          text_size=15, disabled=True, color=colors.WHITE),
                Checkbox(label='1', value=True if settings_data["video_input_type"] == 'file' else False,
                         on_change=input_type, fill_color={
                        MaterialState.HOVERED: LG,
                        MaterialState.FOCUSED: colors.RED,
                        MaterialState.DEFAULT: colors.BLACK,
                    })

            ]),
            Row([
                Text('Video input', size=18, color=colors.WHITE),

                IconButton(icons.ARROW_LEFT, on_click=input_name_update, style=ButtonStyle(color=colors.WHITE)),
                TextButton(settings_data['video_input_name'], disabled=True, style=ButtonStyle(color=colors.WHITE)),
                IconButton(icons.ARROW_RIGHT, on_click=input_name_update, style=ButtonStyle(color=colors.WHITE)),

                Checkbox(label='2', value=True if settings_data["video_input_type"] == 'stream' else False,
                         on_change=input_type,

                         fill_color={
                        MaterialState.HOVERED: LG,
                        MaterialState.FOCUSED: colors.RED,
                        MaterialState.DEFAULT: colors.BLACK,
                    })

            ]),
            Row([
                Text('Video type', size=18, color=colors.WHITE),

                Dropdown(
                    # width=100,
                    value=settings_data['video_type'],
                    scale=0.8,
                    filled=True,

                    options=[
                        dropdown.Option("normal"),
                        dropdown.Option("binary"),
                    ],
                on_change=change_save_button
                )

            ])

        ], expand=True)
    )
    help_page_widget = Container(
        expand=8,
        padding=5,
        border_radius=10,
        bgcolor=BG,
        content=
        Text('Help page', expand=True, color=colors.WHITE)
    )

    def video_settings(e):
        top.content.controls[1].disabled = False
        top.content.controls[1].opacity = 1
        workspace.content.controls[1] = video_settings_widget
        page.update()

    def help_page(e):
        top.content.controls[1].disabled = True
        workspace.content.controls[1] = help_page_widget
        top.content.controls[1].opacity = 0
        page.update()

    workspace = Container(
        expand=True,
        alignment=alignment.top_left,
        bgcolor=colors.TRANSPARENT,
        padding=10,
        content=Row([
            Container(
                border_radius=10,
                bgcolor=BG,
                expand=2,

                content=
                Column([
                    TextButton(content=Text('Video', no_wrap=True), on_click=video_settings),

                    # TextButton(content=Text('Help', no_wrap=True), on_click=help_page),

                ],
                    spacing=0,
                    horizontal_alignment=CrossAxisAlignment.CENTER),

            ),
            video_settings_widget,
        ],
            expand=True)

    )

    inter = Column([top, workspace], expand=True)
    page.add(inter)


if __name__ == "__main__":  # ? This is so important, there will be errors without it.
    app(target=second_target)
