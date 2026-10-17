# Third-party code notices

## pycatia

This repository includes utility scripts copied or adapted from
[pycatia](https://github.com/evereux/pycatia), copyright (c) 2018 Paul Bourne,
and contributions credited in the original files and upstream project.
The original author notices in bundled files are retained.

The bundled upstream code is distributed under the MIT License. The full
upstream license text is included in [user_scripts/LICENSE.txt](user_scripts/LICENSE.txt).
That upstream license applies to the pycatia-derived code. Independently
authored project code, macros and project-owned data are licensed under the
MIT License in the repository root [LICENSE](LICENSE). Original upstream
copyright notices remain applicable.

## ToolFunctions provenance

The upstream source directory corresponding to `user_scripts/ToolFunctions` is
[`user_scripts/wing_surface_from_naca_profile_support`](https://github.com/evereux/pycatia/tree/master/user_scripts/wing_surface_from_naca_profile_support).
The directory was locally renamed to `ToolFunctions`.

Source comparison performed on 2026-10-17:

| Local file under `user_scripts/ToolFunctions/` | Comparison with upstream |
| --- | --- |
| `colour.py` | Identical after ignoring blank lines and trailing whitespace |
| `constants.py` | Identical after ignoring blank lines and trailing whitespace |
| `geometrical_sets.py` | Identical after ignoring blank lines and trailing whitespace |
| `origin_elements.py` | Identical after ignoring blank lines and trailing whitespace |
| `parameters.py` | Identical after ignoring blank lines and trailing whitespace |
| `points.py` | Identical after ignoring blank lines and trailing whitespace |
| `read_dat_file.py` | Identical after ignoring blank lines and trailing whitespace |
| `hide_show.py` | Adapted from upstream; local changes described below |
| `paste_result.py` | Independently authored by the project author, as identified by the author; not part of pycatia |

In `hide_show.py`, the local version adds a `flag=True` argument to
`hide_the_shape` and a `flags=True` argument to `hide_the_shapes`. These
arguments support both showing and hiding shapes, including propagation
through recursive calls.

The upstream `geometrical_sets.py` was also verified in tags
[0.6.4](https://github.com/evereux/pycatia/blob/0.6.4/user_scripts/wing_surface_from_naca_profile_support/geometrical_sets.py)
and
[0.7.3](https://github.com/evereux/pycatia/blob/0.7.3/user_scripts/wing_surface_from_naca_profile_support/geometrical_sets.py).
These matches establish upstream provenance but do not identify the exact
release or commit originally copied. No specific original version is claimed.

Other files bundled under `user_scripts` retain their existing source and
author notices. They were not included in the file-by-file comparison above.

## Project-authored utility

The project author identified `user_scripts/ToolFunctions/paste_result.py` as
their own independently authored utility. It is not attributed to pycatia and
is licensed under the project's root [MIT License](LICENSE), rather than
attributed to the upstream copyright holder.
