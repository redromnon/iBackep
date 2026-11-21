import flet as ft


@ft.component
def OperationDialog(visible: bool, status: str, progress: float | None, finished: bool, on_close):
    operation_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(status, text_align=ft.TextAlign.CENTER),
        content=ft.Container(
            content=ft.ProgressRing(
                value=progress,
                width=60,
                height=60,
                stroke_width=5,
                bgcolor=ft.Colors.GREY,
                color=ft.Colors.WHITE,
            ),
            alignment=ft.Alignment.CENTER,
            height=100,
            width=100,
        ),
        content_padding=30,
        actions=[ft.TextButton("Close", disabled=not finished, on_click=on_close)],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )
    ft.use_dialog(operation_dialog if visible else None)
