from bs4 import BeautifulSoup

from utils import *


class HTMLObfuscator:
    def __init__(self, zero_width_chars_in_text_probability=0.23,
                 zero_width_span_tags_probability=0.23,
                 random_sentence_word_count=21,
                 should_add_zero_width_chars_in_zero_width_span_tags=False,
                 hide_tags_in_style_tag_probability=0.23,
                 should_hide_zero_width_span_tags=False):
        self.zero_width_chars_in_text_probability = zero_width_chars_in_text_probability
        self.zero_width_span_tags_probability = zero_width_span_tags_probability
        self.random_sentence_word_count = random_sentence_word_count
        self.should_add_zero_width_chars_in_zero_width_span_tags = should_add_zero_width_chars_in_zero_width_span_tags
        self.hide_tags_in_style_tag_probability = hide_tags_in_style_tag_probability
        self.should_hide_zero_width_span_tags = should_hide_zero_width_span_tags

    def obfuscate_html(self, html):
        beautiful_soup = BeautifulSoup(html, 'html.parser')
        new_style_tag = beautiful_soup.new_tag("style")
        for element in beautiful_soup.recursiveChildGenerator():
            add_zero_with_chars_into_an_element(element,
                                                self.zero_width_span_tags_probability,
                                                self.should_add_zero_width_chars_in_zero_width_span_tags)
            add_random_span_tag_into_an_element(beautiful_soup,
                                                element,
                                                self.zero_width_span_tags_probability,
                                                self.random_sentence_word_count)
            hide_tag_in_style_tag(beautiful_soup,
                                  element,
                                  self.hide_tags_in_style_tag_probability,
                                  self.should_hide_zero_width_span_tags)
        beautiful_soup.find("body").append(new_style_tag)
        return beautiful_soup.prettify()
