import random

import bs4
from essential_generators import DocumentGenerator

random_sentence_generator = DocumentGenerator()
zero_width_chars = ['​', '‍', '‌']


def _add_zero_width_chars_in_text_with_probability(text, probability=0.4):
    result = ""
    for ch in text:
        random_probability = random.random()
        new_ch = ch
        if random_probability <= probability:
            random_zero_width_char = zero_width_chars[random.randint(0, len(zero_width_chars)-1)]
            new_ch = ch + random_zero_width_char
        result += new_ch

    return result


def _should_change_content(element, skip_class_name=None):
    if skip_class_name is not None:
        if hasattr(element.parent, "attrs"):
            if "class" in element.parent.attrs:
                if skip_class_name in element.parent.attrs["class"]:
                    return False

    if isinstance(element, bs4.element.Stylesheet):
        return False

    if hasattr(element, "parent"):
        if element.parent.name == 'style':
            return False

    if not isinstance(element, bs4.element.NavigableString):
        return False

    if element == '\n':
        return False

    return True


def add_zero_with_chars_into_an_element(element, probability=0.4, should_add_in_inserted_span_tags=False):
    if hasattr(element, 'contents'):
        for i in range(len(element.contents)):
            curr_content = element.contents[i]
            if not _should_change_content(curr_content, "inv" if not should_add_in_inserted_span_tags else None):
                continue
            old_text = str(curr_content)
            new_text = _add_zero_width_chars_in_text_with_probability(
                old_text,
                probability)
            curr_content.replace_with(new_text)


def add_random_span_tag_into_an_element(beautiful_soup, element, probability=0.4, word_count=21):
    random_probability = random.random()
    if random_probability <= probability:
        new_span_tag = beautiful_soup.new_tag("span", attrs={"class": "inv"})
        new_span_tag.append(random_sentence_generator.gen_sentence(1, word_count))
        element.insert_after(new_span_tag)


def hide_tag_in_style_tag(beautiful_soup, element, probability=0.4, should_add_in_inserted_span_tags=False):
    if hasattr(element, 'contents'):
        for i in range(len(element.contents)):
            curr_content = element.contents[i]
            if not _should_change_content(curr_content, "inv" if not should_add_in_inserted_span_tags else None):
                continue
            random_probability = random.random()
            if random_probability <= probability:
                text = str(curr_content)
                new_span_tag = beautiful_soup.new_tag("span", attrs={"class": "css", "d": text})
                curr_content.replace_with(new_span_tag)


def get_new_style_tag(beautiful_soup):
    new_style_tag = beautiful_soup.new_tag("style")
    new_style_tag.append(''' 
        .inv {
            display: none;
        }

        .css::after {
            content: attr(d);
        }''')
    return new_style_tag
