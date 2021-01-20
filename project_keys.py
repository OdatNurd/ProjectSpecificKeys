import sublime
import sublime_plugin

import os
import json


_platform_name = {
    'osx': 'OSX',
    'windows': 'Windows',
    'linux': 'Linux',
}[sublime.platform()]


def plugin_loaded():
    """
    When the plugin loads,  make sure that there's a folder for storing the
    keymap file that we're going to generate.
    """
    os.makedirs(keymap_dir(), exist_ok=True)


def keymap_dir():
    """
    Obtain the folder that we want to generate our keymap files into.
    """
    return os.path.join(sublime.packages_path(), "ProjectSpecificKeys", "keymaps")


def add_context(keymap, project_name):
    """
    Given a key binding, add a context that makes it apply only in the project
    with the given name. If there's not already any context applied to this
    key, then add context to the binding.
    """
    context = keymap.get("context", [])
    context.append({
        "key": "project",
        "operator": "equal",
        "operand": project_name
        })
    keymap["context"] = context
    return keymap


class ProjectSpecificEventListener(sublime_plugin.EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        if key != "project":
            return None

        lhs = view.window().project_file_name()
        if lhs == None:
            return None

        lhs = os.path.split(lhs)[1]
        rhs = operand

        if operator == sublime.OP_EQUAL:
            return lhs == rhs
        elif operator == sublime.OP_NOT_EQUAL:
            return lhs != rhs

        return None

    def on_load_project(self, window):
        data = window.project_data() or {}
        keys = data.get("keys", [])
        if not keys:
            return

        project = os.path.split(window.project_file_name())[1]

        keymap = []
        for key in keys:
            platform = key.pop("platform", None)
            if platform != '!' + _platform_name or platform == _platform_name:
                keymap.append(add_context(key, project))

        try:
            folder = os.path.join(keymap_dir(), project)
            if not os.path.isdir(folder):
                os.mkdir(folder)

            filename = "Default (%s).sublime-keymap" % _platform_name
            filename = os.path.join(folder, filename)
            with open(filename, "w") as file:
                file.write(json.dumps(keymap, indent=4))

        except Exception as e:
            sublime.status_message("Error generating project specific bindings")
            raise e
