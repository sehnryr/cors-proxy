# cors-proxy
A Flask-based proxy that adds CORS headers to every responses.

> **Note**:
> Every headers are forwarded but `Content-Encodind` that causes issues with Flask and [Forbidden headers](https://developer.mozilla.org/en-US/docs/Glossary/Forbidden_header_name). Cookies path are removed as it won't correspond the proxy path.

## Table of Contents

- [cors-proxy](#cors-proxy)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)

## Installation
Install the dependencies with 
```
pip install -r requirements.txt
```

You can either run the proxy with 
```
# for local debugging
python proxy.py

# for production
gunicorn -b 0.0.0.0:8080 server:app
```

Or deploy it with [Fly.io with the Dockerfile](https://fly.io/docs/languages-and-frameworks/dockerfile/). Ensure to [install `flyctl`](https://fly.io/docs/hands-on/install-flyctl/) beforhand.

## Usage
You can then access `http://127.0.0.1:5000/<url>` for any `url` and any HTTP method. The response content and return code will be forwarded.

Example: Access [`https://jsonplaceholder.typicode.com/posts`](https://jsonplaceholder.typicode.com/posts) with [`http://127.0.0.1:5000/https://jsonplaceholder.typicode.com/posts`](http://127.0.0.1:5000/https://jsonplaceholder.typicode.com/posts).
