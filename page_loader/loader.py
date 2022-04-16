import os
from page_loader.creating import create_file_name


def download(url: str, output_dir: str) -> str:
    """Download a web page to a directory

    Args:
        url (str): Web page address.
        output_dir: Path to directory where the web page will be saved.

    Retruns:
        str: Path to saved the web page.
    """

    page_content = get_response(url).text
    file_name = create_file_name(url)
    path_to_file = os.path.join(output_dir, file_name)
    save_web_page(page_content, path_to_file)

    return path_to_file
