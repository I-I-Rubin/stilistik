import sys
import os
import markdown

def markdown_to_html(markdown_text):
    try:
        return markdown.markdown(markdown_text)
    except Exception as e:
        print(f"Error converting Markdown to HTML: {e}")
        return markdown_text

def create_html_table(prefix, output_file):
    german_file = f"{prefix}_de.md"
    english_file = f"{prefix}_en.md"

    if not (os.path.isfile(german_file) and os.path.isfile(english_file)):
        print(f"Error: German or English file not found for prefix {prefix}.")
        return

    with open(german_file, 'r', encoding='utf-8') as german_file:
        german_lines = [line.strip() for line in german_file.readlines()]

    with open(english_file, 'r', encoding='utf-8') as english_file:
        english_lines = [line.strip() for line in english_file.readlines()]

    # Ensure both files have the same number of lines
    if len(german_lines) != len(english_lines):
        print("Error: The German and English files must have the same number of lines.")
        return

    # Open the output HTML file for writing
    with open(output_file, 'w', encoding='utf-8') as html_file:
        # Write HTML header
        html_file.write('<html>\n')
        html_file.write('<head>\n')
        html_file.write('<meta charset="UTF-8"/>\n')
        html_file.write('<link href=\'https://fonts.googleapis.com/css?family=Crimson Text\' rel=\'stylesheet\'>\n')
        html_file.write('<title>')
        html_file.write(prefix)
        html_file.write('</title>\n')
        html_file.write('<style> body {font-family: \'Crimson Text\';font-size: 22px;}</style>\n')
        html_file.write('<style>.left-column { font-size: smaller; width: 25%; }</style>\n<style>.right-column { font-size: x-large; width: 75%; }</style>\n<style>tr { margin-bottom: 1em; }</style>\n<style>table { border-collapse: separate; border-spacing: 10px; width: 100%; }</style>\n</head>\n<body>\n')

        # Write table header
        html_file.write('<table>\n<tr><th style="text-align: left;"> </th><th style="text-align: left;"> </th></tr>\n')

        # Iterate through lines and create table rows
        for german_line, english_line in zip(german_lines, english_lines):
            german_translation = markdown_to_html(german_line)
            english_translation = markdown_to_html(english_line)

            # Write table row with specific classes for the left and right columns
            html_file.write(f'<tr><td class="left-column">{german_translation}</td><td class="right-column">{english_translation}</td></tr>\n')

        # Write HTML footer
        html_file.write('</table>\n</body>\n</html>')

    print(f"HTML table has been created and saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py PREFIX")
    else:
        prefix = sys.argv[1]
        output_file = f"{prefix}.html"
        create_html_table(prefix, output_file)
