import sublime
import sublime_plugin

import os
import json


_platform_name = {
    'osx': 'OSX',
    'windows': 'Windows',
    'linux': 'Linux',
}[sublime.platform()]

_pkg_name = __name__.split('.')[0]


def plugin_loaded():
    """
    When the plugin loads,  make sure that there's a folder for storing the
    keymap file that we're going to generate.
    """
    os.makedirs(keymap_dir(), exist_ok=True)


def project_name(window):
    """
    Return the file name (without extension) for the project currently
    available in the given window.
    """
    if window.project_file_name() is None:
        return None

    return os.path.split(window.project_file_name())[1]


def keymap_dir(project_filename=None):
    """
    Obtain the folder that we want to generate our keymap files into for the
    provided project.
    """
    if project_filename:
        project_filename = os.path.splitext(project_filename)[0]

    return os.path.join(sublime.packages_path(), _pkg_name, "keymaps", project_filename or "")


def keymap_file_path(project_filename):
    """
    Get the fully qualified filename for a key binding file on the current
    platform for the given project filename.
    """
    filename = "Default (%s).sublime-keymap" % _platform_name
    return os.path.join(keymap_dir(project_filename), filename)


def cleanup_keymap(filename=None, folder=None):
    """
    Delete the provided keymap file and, if provided, also remove the
    given directory as well if provided.
    """
    if filename:
        try:
            os.unlink(filename)
        except FileNotFoundError:
            pass

    if folder:
        try:
            os.rmdir(folder)
        except (FileNotFoundError, OSError):
            pass


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

        project = project_name(window)

        keymap = []
        for key in keys:
            platform = key.pop("platform", None)
            if platform != '!' + _platform_name or platform == _platform_name:
                keymap.append(add_context(key, project))

        try:
            folder = keymap_dir(project)
            if keymap and not os.path.isdir(folder):
                os.mkdir(folder)

            filename = keymap_file_path(project)
            if keymap:
                with open(filename, "w") as file:
                    file.write(json.dumps(keymap, indent=4))
            else:
                cleanup_keymap(filename, folder)

        except Exception as e:
            sublime.status_message("Error generating project specific bindings")
            raise e

    def on_pre_close_project(self, window):
        project = project_name(window)
        folder = keymap_dir(project)
        filename = keymap_file_path(project)

        cleanup_keymap(filename, folder)
