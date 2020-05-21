from thonny import get_workbench
import webview

import threading
from multiprocessing import Process

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">

<style>
    #response-container {
        display: none;
        padding: 3rem;
        margin: 3rem 5rem;
        font-size: 120%;
        border: 5px dashed #ccc;
    }

    button {
        padding: 0.5rem;
        margin: 0.3rem;
    }

</style>
</head>
<body>


<h1>Thonny Communication Example</h1>
<p id='pywebview-status'><i>pywebview</i> is not ready</p>
<button onClick="showAndDeleteEditorCode()">Show and Delete Editor Code</button><br/>


<div id="response-container"></div>
<script>
    window.addEventListener('pywebviewready', function() {
        var container = document.getElementById('pywebview-status')
        container.innerHTML = '<i>pywebview</i> is ready'
    })

    function showResponse(response) {
        var container = document.getElementById('response-container')

        container.innerText = response.message
        container.style.display = 'block'
    }

    function showAndDeleteEditorCode() {
        pywebview.api.showAndDeleteEditorCode().then(showResponse)
    }

</script>
</body>
</html>
"""


class Api:
    """This class defines the methods that can be called from Javascript.
        """

    def showAndDeleteEditorCode(self):
        """This method gets the current editor content and sets the content to an empty string.

        Returns:
            JSON response with the editor content
        """
        response = {
            "message": str(
                get_workbench().get_editor_notebook().get_current_editor_content()
            )
        }
        get_workbench().get_editor_notebook().get_current_editor().get_code_view().set_content(
            ""
        )
        return response


def start_webview():
    """This method gets called once the new thread is created. It starts the webview
       and Javascript API.

        Returns:
            None
        """
    api = Api()
    webview.create_window("Example", html=html, js_api=api)
    webview.start(gui="qt")


def commandHandler():
    """This method gets called if the webview item is called in the tools menu.

        Returns:
            None
        """

    # Starting the webview in a new thread works with the qt GUI backend only if
    # the webview is started once. If you try to start it another time, thonny and the
    # webview will crash. This is especially annoying because unsaved work will be gone
    # and cannot be recovered. The name of the thread has to be MainThread or else the
    # webview will not start. The GTK and cef GUI backends do not work with threads.
    t = threading.Thread(target=start_webview, name="MainThread")
    t.daemon = True
    t.start()

    # Starting the webview in a new process will result in thonny blocking.
    # Communication with thonny does not work as well. Thonny remains blocking even if
    # the webview is closed.
    # p = Process(target=start_webview)
    # p.start()
    # p.join()


def load_plugin():
    """This method gets called if this plugin is in the PYTHONPATH environment variable
       upon starting thonny. This code is executed before TK windows are drawn. That is
       why you should use add a command to the thonny GUI before running anything.

        Returns:
            None
        """
    get_workbench().add_command(
        command_id="webview",
        menu_name="tools",
        command_label="Start Webview",
        handler=commandHandler,
    )

    # Running a webview in this function will result in a working webview but the
    # thonny GUI is not drawn until the webview is closed. The communication with the
    # thonny IDE will also not work.
    # webview.create_window(
    #     "Webview Title", "https://tu-dresden.de/ing/informatik/smt/ddi"
    # )
    # webview.start(func=start_webview, gui="cef")
