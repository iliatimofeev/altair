import os

from ...utils import PluginRegistry
from ..display import Displayable
from ..display import default_renderer_base
from ..display import json_renderer_base
from ..display import RendererType



# ==============================================================================
# Vega 4 renderer logic
# ==============================================================================


# The MIME type for Vega 3 releases.
VEGA_MIME_TYPE = 'application/vnd.vega.v4+json'  # type: str

# The entry point group that can be used by other packages to declare other
# renderers that will be auto-detected. Explicit registration is also
# allowed by the PluginRegistery API.
ENTRY_POINT_GROUP = 'altair.vega.v4.renderer'  # type: str

# The display message when rendering fails
DEFAULT_DISPLAY = """\
<Vega 4 object>

If you see this message, it means the renderer has not been properly enabled
for the frontend that you are using. For more information, see
https://altair-viz.github.io/user_guide/troubleshooting.html
"""

renderers = PluginRegistry[RendererType](entry_point_group=ENTRY_POINT_GROUP)


here = os.path.dirname(os.path.realpath(__file__))


def default_renderer(spec):
    return default_renderer_base(spec, VEGA_MIME_TYPE, DEFAULT_DISPLAY)


def json_renderer(spec):
    return json_renderer_base(spec, DEFAULT_DISPLAY)


renderers.register('default', default_renderer)
renderers.register('jupyterlab', default_renderer)
renderers.register('nteract', default_renderer)
renderers.register('json', json_renderer)
renderers.enable('default')


class Vega(Displayable):
    """An IPython/Jupyter display class for rendering Vega 3."""

    renderers = renderers
    schema_path = (__name__, 'schema/vega-schema.json')


def vega(spec, validate=True):
    """Render and optionally validate a Vega 34spec.

    This will use the currently enabled renderer to render the spec.

    Parameters
    ==========
    spec: dict
        A fully compliant Vega 4 spec, with the data portion fully processed.
    validate: bool
        Should the spec be validated against the Vega 4 schema?
    """
    from IPython.display import display

    display(Vega(spec, validate=validate))
