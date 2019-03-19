import pytest

from eruditarticle.utils import normalize_whitespace


@pytest.mark.parametrize('s1, s2', [
    ('foo  bar', 'foo bar'),
    (' foo  bar ', 'foo bar'),
    ('foo\nbar', 'foo bar'),
    ('foo\n\t bar', 'foo bar'),
    # We don't want to normalize unbreakable spaces. Keeping them is important.
    ('foo\xa0bar', 'foo\xa0bar'),
])
def test_normalize_whitespaces(s1, s2):
    assert normalize_whitespace(s1) == s2
