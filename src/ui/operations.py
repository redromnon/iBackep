import flet as ft, time
from libutilities import Action

class Operation(ft.UserControl):
    
    def build(self):
        
        self.action = Action()
        
        self.lib_output = ft.TextField(value="", filled=True, read_only=True, multiline=True, text_size=13, color=ft.colors.AMBER)
        
        self.close_button = ft.TextButton("Close", disabled=True, on_click=self.close_dialog)
        self.cancel_button = ft.TextButton("Cancel", disabled=False, on_click=self.cancel_op)

        self.loading = ft.ProgressBar()
        
        self.result_dialog = ft.AlertDialog(
            content=ft.Column(
                [
                    self.loading,
                    ft.Column(
                        [self.lib_output], 
                        horizontal_alignment="center", expand=True, auto_scroll=True, scroll="auto",
                        width=600
                    ),
                ], width=600
            ),
            content_padding=30, modal=True,
            actions=[self.close_button, self.cancel_button]
        )

        return self.result_dialog

    def backup(self, folder, pwd):

        self.result_dialog.open = True
        self.result_dialog.title = ft.Text("Backing Up", text_align="center")
        self.lib_output.value = "Running backup...\n"
        self.update()

        process = self.action.backup(folder, pwd)
       
        while True:

            #Benefits smoother scrolling of lib_output texfield
            time.sleep(0.5)
            line = process.stdout.readline().decode()

            print(line, end='')        
            self.lib_output.value += line
            self.update()

            if process.poll() is not None and line == '':
                break

        self.close_button.disabled = False
        self.cancel_button.disabled = True
        self.loading.value = 0.0
        self.update()

    
    def restore(self, folder, pwd):

        self.result_dialog.open = True
        self.result_dialog.title = ft.Text("Restoring", text_align="center")
        self.lib_output.value = "Running restore...\n"
        self.update()

        process = self.action.restore(folder, pwd)

        while True:

            #Benefits smoother scrolling of lib_output texfield
            time.sleep(0.5)
            line = process.stdout.readline().decode()

            print(line, end='')        
            self.lib_output.value += line
            self.update()

            if process.poll() is not None and line == '':
                break

        self.close_button.disabled = False
        self.cancel_button.disabled = True
        self.loading.value = 0.0
        self.update()


    def close_dialog(self, e):

        #Reset properties to default
        self.lib_output.value = ""
        self.close_button.disabled = True
        self.cancel_button.disabled = False
        self.loading.value = None
        self.result_dialog.open = False
        self.update()


    def cancel_op(self, e):

        self.lib_output.value += "\n--CANCELLED BY USER--"
        self.loading.value = 0.0
        self.update()

        self.action.cancel()

        

