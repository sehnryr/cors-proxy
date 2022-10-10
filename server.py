# -*- coding: utf-8 -*-


import flask
import flask_cors
import requests

app = flask.Flask(__name__)

available_methods = [
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "PATCH",
    "OPTIONS",
]

# https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_header_name
# https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_response_header_name
forbidden_headers = [
    "accept-charset",
    "accept-encoding",
    "access-control-request-headers",
    "access-control-request-method",
    "connection",
    "content-length",
    "cookie",
    "cookie2",
    "date",
    "dnt",
    "expect",
    "feature-policy",
    "host",
    "keep-alive",
    "origin",
    "set-cookie",
    "referer",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "via",
]


def filter_headers(headers):
    """
    Filters the headers to remove forbidden headers
    """
    return {
        k.lower(): v
        for k, v in headers.items()
        if k.lower() not in forbidden_headers
        and not k.lower().startswith("proxy-")
        and not k.lower().startswith("sec-")
    }


@app.route("/<path:url>", methods=available_methods)
@flask_cors.cross_origin(
    expose_headers="*",
    supports_credentials=True,
)
def proxy(url):
    session = requests.Session()
    response = session.request(
        method=flask.request.method,
        url=url,
        stream=True,
        params=flask.request.args.to_dict(),
        data=flask.request.form.to_dict(),
        cookies=flask.request.cookies,
    )

    headers = filter_headers(response.headers)
    # Add proxy url to the location header if exists
    if "location" in headers.keys():
        headers["location"] = flask.request.host_url + headers["location"]

    # Remove the content-length header if exists as it is buggy when set
    headers.pop("content-encoding", None)
    headers.pop("content-type", None)

    custom_response = flask.Response(
        flask.stream_with_context(response.iter_content()),
        content_type=response.headers["content-type"]
        if "content-type" in response.headers.keys()
        else None,
        headers=headers,
        status=response.status_code,
    )
    for cookie in session.cookies:
        custom_response.set_cookie(
            key=cookie.name,
            value=cookie.value,
            expires=cookie.expires,
        )
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
    app.run()
