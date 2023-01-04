from src.hoge.app import hoge


def test_hoge():
    actual = hoge()

    assert actual == "a"
