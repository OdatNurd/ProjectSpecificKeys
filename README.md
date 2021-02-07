ProjectSpecificKeys
===================

This is a prototype of a package that was originally implemented during [Live Stream #57](https://youtu.be/XmqwGQZxSPY)
on my [secondary channel on YouTube](https://www.youtube.com/c/TerenceMartinLive)
and then worked on in some subsequent streams.

This requires a build of Sublime Text >= 4050 (i.e. not Sublime Text 3) due to
using some new API endpoints not available in older versions.


Usage
-----

This package allows you to include key bindings inside of a `sublime-project`
file via a new `"keys"` key. Whenever this project is open inside of a window,
the key bindings in that project will be in effect in that window.

The menu command `Preferences > Key Bindings - Project Specific` or the command
palette entry `ProjectSpecificKeys: Project Key Bindings` can be used to open
the current project to allow inserting keys.

    > ***NOTE***: The first time you use this command in a new project, you need
      to manually include a `"keys"` key to store the bindings in.

An example of project specific bindings in use is:

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
            "keys": ["ctrl+shift+h"], "command": "echo", "args": {
                "message": "I only work in this project"
            }
        },
    ],
}
```

The value of `"keys"` should be a list of key bindings, in the same format and
manner as you would put them into the standard user key bindings. `"keys"` is
not normally present in a project; you will need to add it yourself if it is
not already there.

Every time the package changes, the key bindings in it will be updated in Sublime
and become active, allowing for the same keys to be used in different windows
in a manner specific to the project that you're working within.


Platform Specific Bindings
--------------------------

Normally when you define key bindings in Sublime, they go into your platform
specific key bindings, allowing you to synchronize your `User` package across
multiple platforms and ensure that bindings are only applied on the platforms
they're intended for.

By default, any keys that you add to the project will be applied no matter what
platform the project is being used on. If you develop across multiple platforms
(or you are working with people who are on other platforms and also use this
package), it is possible to specify key bindings in a platform specific kay.

To do this, include a `"platform"` key in your key binding, with one of the
following values:

  * `"Linux"`, `"Windows"` or `"OSX"` if the key binding should apply to only
    that specific platform

  * `"!Linux"`, `"!Windows"` or `"!OSX"` if the key binding should apply to
    any platform except the one provided.


For example:

```json
    "keys": [
        {
            "platform": "!OSX",
            "keys": ["ctrl+shift+h"], "command": "echo", "args": {
                "message": "I only work in this project on Linux and Windows"
            }
        },
        {
            "platform": "OSX",
            "keys": ["super+h"], "command": "echo", "args": {
                "message": "I only work in this project on MacOS"
            }
        },

    ],
````

Here the first key binding will apply only on Linux and Windows and the second
will apply only on MacOS. This allows you to constrain bindings to the platform
they're intended for, such as to use different keys for the same actions (as
in the example above) or in cases where an operation only makes sense on some
platforms and not others.
