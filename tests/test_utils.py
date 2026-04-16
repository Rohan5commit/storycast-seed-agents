from storycast.utils import extract_json_object, slugify


def test_extract_json_object_handles_markdown_fence() -> None:
    raw = "\n".join(["```json", '{"title": "Nebula"}', "```"])
    assert extract_json_object(raw) == '{"title": "Nebula"}'


def test_slugify_normalizes_plain_english_topics() -> None:
    assert slugify("The Death of a Star!") == "the-death-of-a-star"
