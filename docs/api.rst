Use this format: https://gist.github.com/iros/3426278
=========
MODUA API
=========

Show Languages
==============

URL
---

/api/0.1/languages/


Method
------

::    
    GET

        
URL Params
----------

`Required`::

        None

`Optional`::

        None


.. todo::

        Implement optional id parameter


Example
-------

::

        GET :8000/api/0.1/languages/


        HTTP/1.0 200 OK
        Allow: GET, HEAD, OPTIONS
        Content-Type: application/json
        Date: Wed, 07 Sep 2016 17:45:48 GMT
        Server: WSGIServer/0.2 CPython/3.5.2
        Vary: Accept, Cookie
        X-Frame-Options: SAMEORIGIN

        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 3,
                    "language": "zh"
                },
                {
                    "id": 4,
                    "language": "en"
                }
            ]
        }


Show User Definitions
=====================

URL
---

/api/0.1/languages/:language/definitions/:word/ 'Authorization: Token <token>'


Method
------

::
    GET


URL Params
----------

`Required`::

        None


`Optional`::

        id=[integer]


Examples
========


Getting A User's Token
----------------------

Assume there already is a user `foo` with password `password`.  First, get foo's token by posting his username/password::

    POST :8000/api/0.1/api-token-auth/ username=foo password=password


        HTTP/1.0 200 OK
        Allow: POST, OPTIONS
        Content-Type: application/json
        Date: Wed, 07 Sep 2016 17:22:43 GMT
        Server: WSGIServer/0.2 CPython/3.5.2
        Vary: Cookie
        X-Frame-Options: SAMEORIGIN

        {
            "token": "7b77c7031b4da70722f4eaeb7a54cbaa2fe25209"
        }


Getting A User Created Definition
---------------------------------


 To access a definition that user `foo` made for the word `未完成`, use the following request.

`Request`::

        GET /api/0.1/languages/zh/definitions/未完成/ 'Authorization: Token 7b77c7031b4da70722f4eaeb7a54cbaa2fe25209'

`Response`::

        HTTP/1.0 200 OK
        Allow: GET, HEAD, OPTIONS
        Content-Type: application/json
        Date: Wed, 07 Sep 2016 17:33:41 GMT
        Server: WSGIServer/0.2 CPython/3.5.2
        Vary: Accept
        X-Frame-Options: SAMEORIGIN

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "definition": "defininition for 未完成",
                    "id": 38120,
                    "language": {
                        "id": 3,
                        "language": "zh"
                    },
                    "word": {
                        "ease": "new",
                        "id": 33259,
                        "language": {
                            "id": 3,
                            "language": "zh"
                        },
                        "word": "未完成"
                    },
                    "word_type": null
                }
            ]
        }


Deleting A User Created Definition
---------------------------------


.. todo::

        Implement DELETE request on user definition


Getting Public Definitions
--------------------------

To access all public definitions (not created by users), use the same request as for private definitions but without a token.

`Request`::


        GET /api/0.1/languages/zh/definitions/未完成/


`Result`::

        HTTP/1.0 200 OK
        Allow: GET, HEAD, OPTIONS
        Content-Type: application/json
        Date: Wed, 07 Sep 2016 17:33:24 GMT
        Server: WSGIServer/0.2 CPython/3.5.2
        Vary: Accept
        X-Frame-Options: SAMEORIGIN

        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "definition": "public definition for 未完成",
                    "id": 38502,
                    "language": {
                        "id": 4,
                        "language": "en"
                    },
                    "word": {
                        "ease": "",
                        "id": 33640,
                        "language": {
                            "id": 3,
                            "language": "zh"
                        },
                        "word": "未完成"
                    },
                    "word_type": null
                }
            ]
        }


Parsing A String
----------------


::

        POST :8000/api/0.1/languages/zh/parse/ string=一套由于实现

        HTTP/1.0 200 OK
        Allow: POST, OPTIONS
        Content-Type: application/json
        Date: Wed, 07 Sep 2016 18:05:12 GMT
        Server: WSGIServer/0.2 CPython/3.5.2
        Vary: Accept, Cookie
        X-Frame-Options: SAMEORIGIN

        [
            {
                "position": 0,
                "string": "一套"
            },
            {
                "position": 1,
                "string": "由于"
            },
            {
                "position": 2,
                "string": "实现"
            }
        ]
