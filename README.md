# ProjectSpecificKeys

This is a prototype of a package implemented during [Live Stream #57](https://youtu.be/XmqwGQZxSPY)
on my [secondary channel on YouTube](https://www.youtube.com/c/TerenceMartinLive),
and currently does two things.

With this package, you can include a `"keys"` key in your `sublime-project` file
to specify key bindings that you want to have available inside of windows that
have that project loaded. For example:

```json
{
    "folders":
    [
        {
            "path": "."
        }
    ],
    "keys": [
        {
            "keys": ["super+t"], "command": "echo", "args": {
                "project": "Project Specific"
            }
        },
    ],
}
```

The package listens for the event that indicates that a project file was loaded
(or reloaded, if you modify the file) and generates a keymap file for the keys
contained inside. The keymap is generated inside of
`Packages/ProjectSpecificKeys/keymaps`, and as each keymap is written out a
context is added that makes it specific to windows with the project loaded.

The plugin also includes a context that makes a key binding apply only in a
window where the project file is loaded. This could also be used in general
outside of this package (for example in Sublime Text 3) if you wanted to
manually create your key bindings instead.

This package is still a proof of concept, so while this works, there are other
things that need to be added to it to make it more functional for the masses.
For example:

* Key binding files are created, but never cleaned up. Some mechanism to get
  rid of files would probably be a good thing

* Key bindings are always specific to the current platform. If you use Sublime
  across multiple platforms, you might want to have platform specific key
  bindings. The live stream replay linked above shows some examples of what this
  might look like, but it has not been implemented yet.

This requires a build of Sublime Text >= 4050 (possibly higher; but basically
this will not work in Sublime Text 3) due to using some new API endpoints not
available in older versions.
