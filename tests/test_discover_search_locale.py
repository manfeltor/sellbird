"""icp.search_country / search_language reach the search providers."""

from types import SimpleNamespace

from sellbird.collectors.discover import DiscoveryQuery, _serper_payload, build_queries


def _config(**icp):
    base = dict(industries=["importador"], geography=["Ciudad Ejemplo"],
                keyword_variants={}, geo_coordinates={})
    base.update(icp)
    return SimpleNamespace(icp=SimpleNamespace(**base),
                           product=SimpleNamespace(name="Example"))


def test_build_queries_carries_country_and_language():
    q = build_queries(_config(search_country=" AR ", search_language="ES"))[0]
    assert (q.country, q.language) == ("ar", "es")


def test_build_queries_defaults_to_empty():
    q = build_queries(_config())[0]
    assert (q.country, q.language) == ("", "")


def test_serper_payload_sets_gl_hl_only_when_given():
    plain = _serper_payload(DiscoveryQuery(term="importador", location="Ciudad Ejemplo"))
    assert "gl" not in plain and "hl" not in plain
    local = _serper_payload(DiscoveryQuery(term="importador", country="ar", language="es"))
    assert local["gl"] == "ar" and local["hl"] == "es" and local["num"] == 10
