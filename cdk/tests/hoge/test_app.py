from src.hoge.app import hoge


def test_hoge():
    actual = hoge()

    assert actual == "a"


def test_hoge2():
    actual = hoge()

    assert actual == "b"
