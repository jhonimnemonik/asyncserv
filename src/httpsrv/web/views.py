import os


def read_html_file(file_name):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


async def home(request):
    html_content = read_html_file("home.html")
    return html_content


async def about(request):
    html_content = read_html_file("about.html")
    return html_content
