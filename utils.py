import textwrap

def print_text_wrapped(text, max_chars_per_line=90):
    """
    Prints a given text string, wrapping it to a maximum number of characters per line.
    Handles existing line breaks and very long lines by breaking words if necessary.

    Args:
        text (str): The input string.
        max_chars_per_line (int): The maximum number of characters allowed per line.
    """

    # Replace existing line breaks with a space to allow textwrap to re-wrap properly,
    # then split the text into "paragraphs" by double line breaks (or more).
    # This helps preserve intentional paragraph breaks.
    paragraphs = text.replace('\r\n', '\n').split('\n\n')

    for para in paragraphs:
        # For each paragraph, further split by single line breaks and re-wrap
        # to ensure even lines within a paragraph are handled.
        sub_lines = para.split('\n')
        for sub_line in sub_lines:
            # Use textwrap.fill to handle the actual wrapping.
            # break_long_words=True ensures that if a single word is longer
            # than max_chars_per_line, it will be broken.
            wrapped_line = textwrap.fill(sub_line,
                                         width=max_chars_per_line,
                                         break_long_words=True,
                                         replace_whitespace=True)
            print(wrapped_line)
        # Add an extra line break between original paragraphs
        if para != paragraphs[-1]: # Don't add an extra line break after the last paragraph
            print()
