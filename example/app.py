import ujson
from sanic import Sanic
from sanic.response import html
from sanic_babel import Babel, force_locale
from sanic_babel import gettext as _

from sanic_aioja import FileSystemLoader, Jinja2

app = Sanic("sanic_aioja")
app.static("/static", "./static")

jinja2 = Jinja2(
    app,

    # use DebugUndefined
    debug=True,

    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader("templates"),
).policies({
    'ext.i18n.trimmed': True,
    'json.dumps_function': ujson.dumps
}).globals({
    'token': 'extensions.token',
}).filters({
    'shuffle': 'extensions.shuffle',
}).tests({
    'digit': 'extensions.is_digit',
}).extensions({
    'extensions.ReverseExtension',
})

babel = Babel(app)


@app.route('/')
@jinja2.template("index.html")
async def index(request):
    return {
        "header": "Sanic-aioja",
        "array": ["Red", "Green", "Blue"],
    }


@app.route('/render/')
async def manual_render(request):
    content = await jinja2.render_to_string(request, "index.html", {
        "header": "Sanic-aioja (render_to_string)",
        "array": ["Yellow", "Pink", "Silver"],
    })
    return html(content)


@app.route('/ru/')
@jinja2.template('index.html')
async def ru_locale(request):
    with force_locale('ru', request):
        content = await jinja2.render_to_string(request, 'index.html', {
            'header': 'Sanic-aioja',
            'array': [
                _('Red', request),
                _('Green', request),
                _('Blue', request)
            ],
        })
    return html(content)


@app.route('/test-404/')
@jinja2.template("index.html")
async def return_response(request):
    return html("404 - Not Found", status=404)


if __name__ == "__main__":
    app.run()
