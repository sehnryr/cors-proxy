# -*- coding: utf-8 -*-


from http import cookies
import flask
import requests
from requests.structures import CaseInsensitiveDict

app = flask.Flask(__name__)

method_requests_mapping = {
    "GET": requests.get,
    "HEAD": requests.head,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete,
    "PATCH": requests.patch,
    "OPTIONS": requests.options,
}


@app.route("/<path:url>", methods=method_requests_mapping.keys())
def proxy(url):
    requests_function = method_requests_mapping[flask.request.method]
    response = requests_function(
        url,
        stream=True,
        params=flask.request.args,
        allow_redirects=False,
    )
    custom_response = flask.Response(
        flask.stream_with_context(response.iter_content()),
        content_type=response.headers["content-type"]
        if "content-type" in response.headers.keys()
        else None,
        status=response.status_code,
    )
    custom_response.headers["Access-Control-Allow-Origin"] = "*"
    return custom_response


@app.errorhandler(404)
def help_message(e):
    message = """
Usage:

/       Shows this help message
/<url>  Make a request to <url>

Source code : https://github.com/sehnryr/cors-proxy
    """.strip()

    response = flask.make_response(message, 400)
    response.mimetype = "text/plain"
    return response


@app.errorhandler(Exception)
def default(e):
    message = "The URL scheme is neither HTTP nor HTTPS"

    response = flask.make_response(message, 400)
    response.mimetype = "text/plain"
    return response


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
