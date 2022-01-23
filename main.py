# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from HTMLObfuscator import HTMLObfuscator
import optparse

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-i', help='arguments', dest='html_input_file_path', action='store')
    parser.add_option('-o', help='arguments', dest='html_output_file_path', action='store')
    (opts, args) = parser.parse_args()
    html_input_file_path = opts.html_input_file_path
    html_output_file_path = opts.html_output_file_path
    html_obfuscator = HTMLObfuscator()
    with open(html_input_file_path, "r") as f:
        html = f.read()
    html_obf = html_obfuscator.obfuscate_html(html)
    with open(html_output_file_path, "w", encoding="utf-8") as f:
        f.write(html_obf)
