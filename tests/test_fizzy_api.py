import pytest

from xian_tech import fizzy_api


def test_external_pagination_url_is_rejected_before_sending_token(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("must not send a request to another origin")

    monkeypatch.setattr(fizzy_api, "build_opener", forbidden)
    with pytest.raises(ValueError, match="origin"):
        fizzy_api._request_json(
            "https://tasks.example", "1", "secret", "https://other.example/cards"
        )


def test_pagination_cycle_stops_before_repeated_request(monkeypatch):
    calls = []

    def request(*args):
        calls.append(args[3])
        assert len(calls) < 3, "unbounded pagination cycle"
        return [{"id": 1}], {"Link": '<https://tasks.example/1/cards>; rel="next"'}

    monkeypatch.setattr(fizzy_api, "_request_json", request)
    with pytest.raises(ValueError, match="cycle"):
        fizzy_api.get_paginated("https://tasks.example", "1", "secret", "/cards")
    assert len(calls) == 1


def test_redirect_does_not_forward_auth_to_another_origin():
    request = fizzy_api.Request(
        "https://tasks.example/1/cards", headers={"Authorization": "Bearer secret"}
    )
    handler = fizzy_api._SameOriginRedirect("https://tasks.example")
    with pytest.raises(ValueError, match="origin"):
        handler.redirect_request(request, None, 302, "redirect", {}, "https://other.example/cards")
    redirected = handler.redirect_request(
        request, None, 302, "redirect", {}, "https://tasks.example/next"
    )
    assert redirected.get_header("Authorization") == "Bearer secret"


def test_relative_links_and_lowercase_headers(monkeypatch):
    calls = []

    def request(base, account, token, path, params):
        calls.append(path)
        return ([{"id": len(calls)}], {"link": '<?page=2>; rel="next"'} if len(calls) == 1 else {})

    monkeypatch.setattr(fizzy_api, "_request_json", request)
    assert fizzy_api.get_paginated("https://tasks.example", "1", "secret", "/cards") == [
        {"id": 1},
        {"id": 2},
    ]
    assert calls == ["https://tasks.example/1/cards", "https://tasks.example/1/cards?page=2"]


def test_page_limit_stops_endless_distinct_links(monkeypatch):
    calls = []
    monkeypatch.setattr(fizzy_api, "MAX_PAGES", 2)

    def request(*args):
        calls.append(args[3])
        return [], {"Link": f'<?page={len(calls) + 1}>; rel="next"'}

    monkeypatch.setattr(fizzy_api, "_request_json", request)
    with pytest.raises(ValueError, match="page limit"):
        fizzy_api.get_paginated("https://tasks.example", "1", "secret", "/cards")
    assert len(calls) == 2


@pytest.mark.parametrize(
    "url",
    [
        "http://tasks.example/cards",
        "https://tasks.example:444/cards",
        "https://tasks.example:0/cards",
        "https://user:secret@tasks.example/cards",
        "file:///tmp/cards",
    ],
)
def test_endpoint_restrictions(url):
    with pytest.raises(ValueError):
        fizzy_api._require_same_origin("https://tasks.example", url)
