# -*- coding: utf-8 -*-
import os
import sys
from nepterm import exec

# For Linux/Wayland users.
if os.getenv("XDG_SESSION_TYPE") == "wayland":
    os.environ["XDG_SESSION_TYPE"] = "x11"

import glfw
import OpenGL.GL as gl
import imgui
from json import load
from imgui.integrations.glfw import GlfwRenderer

FILE_EXPLORER_DEFAULT_FILE_PATH = os.getcwd()

with open("parameters.json") as file:
    parameters = load(file)

try:
    FILE_EXPLORER_DEFAULT_FILE_PATH = parameters["file explorer"]["default file path"]
except:
    pass

path_to_font = None  # "path/to/font.ttf"

active_file_explorer = [FILE_EXPLORER_DEFAULT_FILE_PATH]
active_document_viewer = []
active_text_editor = []
active_terminal = []
active_settings = False


def open_settings():
    imgui.begin("Settings")
    imgui.text("Hello, World!")
    imgui.end()

def open_terminal(file_path: str, window_name: str):
    pass

def open_text_editor(file_path: str, window_name: str = None):
    if window_name == None:
        window_name = f"T @ {file_path}"
    global active_text_editor
    _, is_active = imgui.begin(window_name, closable=True)
    imgui.begin_group()
    if not is_active:
        active_text_editor.remove(file_path)
    else:
        with open(file_path, "r") as file:
            value = "".join(file.readlines())
        is_changed, text = imgui.input_text_multiline(
            "##label",
            value,
            width=-1,
            height=-1,
            flags=imgui.INPUT_TEXT_AUTO_SELECT_ALL | imgui.INPUT_TEXT_ALLOW_TAB_INPUT,
        )
        io = imgui.get_io()
        # save
        if io.key_ctrl and io.keys_down[glfw.KEY_S]:
            if is_changed:
                with open(file_path, "w") as file:
                    parsed = text.split("\n")
                    for i in range(len(parsed) - 1):
                        parsed[i] = parsed[i].rstrip() + "\n"
                    file.writelines(parsed)
    imgui.end_group()
    imgui.end()


def open_document_viewer(file_path: str, window_name: str = None):
    if window_name == None:
        window_name = f"V @ {file_path}"
    global active_document_viewer, active_text_editor
    _, is_active = imgui.begin(window_name, closable=True)
    if not is_active:
        active_document_viewer.remove(file_path)
    else:
        if imgui.button("Edit"):
            active_text_editor.append(file_path)
        imgui.same_line()
        imgui.text("Read only mode")
        with open(file_path, "r") as file:
            value = "".join(file.readlines())
        imgui.input_text_multiline(
            "##label",
            value,
            width=-1,
            height=-1,
            flags=imgui.INPUT_TEXT_AUTO_SELECT_ALL | imgui.INPUT_TEXT_READ_ONLY,
        )
    imgui.end()


def open_file_explorer(file_path: str, window_name: str = None):
    if window_name == None:
        window_name = f"X @ {file_path}"
    global active_file_explorer, active_document_viewer
    window_name = f"X @ {file_path}"
    _, is_active = imgui.begin(
        window_name,
        closable=True,
        flags=imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_ALWAYS_AUTO_RESIZE,
    )
    if not is_active:
        active_file_explorer.remove(file_path)
        imgui.end()
        return
    imgui.begin_group()
    imgui.begin_child(
        "files",
        height=350,
        border=True,
        flags=imgui.WINDOW_ALWAYS_VERTICAL_SCROLLBAR
        | imgui.WINDOW_ALWAYS_HORIZONTAL_SCROLLBAR,
    )
    files = [file for file in os.listdir(file_path)]
    # for current working directory
    imgui.push_style_color(imgui.COLOR_BUTTON, r=0.396, g=0.454, b=0.196)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, r=0.36, g=0.66, b=0.02)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, r=0.396, g=0.454, b=0.196)
    if imgui.button("."):
        pass
    imgui.pop_style_color()
    imgui.pop_style_color()
    imgui.pop_style_color()

    # for parent working directory
    imgui.push_style_color(imgui.COLOR_BUTTON, r=0.396, g=0.454, b=0.196)
    imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, r=0.36, g=0.66, b=0.02)
    imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, r=0.396, g=0.454, b=0.196)
    if imgui.button(".."):
        os.chdir(f"{file_path}/..")
        active_file_explorer.remove(file_path)
        file_path = os.getcwd()
        active_file_explorer.append(file_path)
    imgui.pop_style_color()
    imgui.pop_style_color()
    imgui.pop_style_color()

    for file in files:
        if file == "imgui.ini":
            continue
        if not os.path.isfile(file):
            imgui.push_style_color(imgui.COLOR_BUTTON, r=0.396, g=0.454, b=0.196)
            imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, r=0.36, g=0.66, b=0.02)
            imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, r=0.396, g=0.454, b=0.196)
            if imgui.button(file):
                os.chdir(f"{file_path}/{file}")
                active_file_explorer.remove(file_path)
                file_path = os.getcwd()
                active_file_explorer.append(file_path)
            imgui.pop_style_color()
            imgui.pop_style_color()
            imgui.pop_style_color()
        else:
            if imgui.button(file):
                active_document_viewer.append(f"{file_path}/{file}")
    imgui.end_child()
    enter_pressed, command = imgui.input_text(
        "Console", "", flags=imgui.INPUT_TEXT_ENTER_RETURNS_TRUE
    )
    if enter_pressed:
        os.system(command)
    imgui.same_line()
    if imgui.button("Open in terminal"):
        pass
    imgui.end_group()
    imgui.end()


def handle_key_press():
    io = imgui.get_io()

    # exit
    if io.key_ctrl and io.keys_down[glfw.KEY_W]:
        sys.exit(0)
    # new file explorer
    if io.key_ctrl and io.keys_down[glfw.KEY_X]:
        # active_file_explorer.append(FILE_EXPLORER_DEFAULT_FILE_PATH)
        pass


def frame_commands():
    global active_file_explorer, active_text_editor
    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    handle_key_press()

    if imgui.begin_main_menu_bar():
        if imgui.begin_menu("File", True):
            clicked_settings, selected_settings = imgui.menu_item(
                "Settings", "Ctrl+S", False, True
            )
            clicked_exit, _ = imgui.menu_item("exit", "Ctrl+W", False, True)
            if clicked_exit:
                sys.exit(0)
            if clicked_settings:
                open_settings()
            imgui.end_menu()
        if imgui.begin_menu("New", True):
            if imgui.menu_item("File explorer", "Ctrl+X", False, True)[0]:
                # active_file_explorer.append(FILE_EXPLORER_DEFAULT_FILE_PATH)
                pass
            if imgui.menu_item("Terminal", "Ctrl+T", False, True)[0]:
                pass
            if imgui.menu_item("Text editor", "Ctrl+E", False, True)[0]:
                pass
            imgui.end_menu()
        imgui.end_main_menu_bar()

    file_explorer_dict = dict()
    for fe in active_file_explorer:
        if fe not in file_explorer_dict:
            open_file_explorer(fe)
            file_explorer_dict[fe] = 1
        else:
            open_file_explorer(fe, window_name=f"X @ {fe} ({file_explorer_dict[fe]})")
            file_explorer_dict[fe] += 1
    for te in active_text_editor:
        open_text_editor(te)
    for dv in active_document_viewer:
        open_document_viewer(dv)


def render_frame(impl, window, font):
    glfw.poll_events()
    impl.process_inputs()
    imgui.new_frame()

    gl.glClearColor(0.1, 0.1, 0.1, 1)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    if font is not None:
        imgui.push_font(font)
    frame_commands()
    if font is not None:
        imgui.pop_font()

    imgui.render()
    impl.render(imgui.get_draw_data())
    glfw.swap_buffers(window)


def impl_glfw_init():
    width, height = 1600, 900
    window_name = "Neptune"

    if not glfw.init():
        print("Could not initialize OpenGL context")
        sys.exit(1)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        sys.exit(1)

    return window


def main():
    imgui.create_context()
    window = impl_glfw_init()

    impl = GlfwRenderer(window)

    io = imgui.get_io()
    jb = (
        io.fonts.add_font_from_file_ttf(path_to_font, 30)
        if path_to_font is not None
        else None
    )
    impl.refresh_font_texture()

    while not glfw.window_should_close(window):
        render_frame(impl, window, jb)

    impl.shutdown()
    glfw.terminate()


if __name__ == "__main__":
    main()
