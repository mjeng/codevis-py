from bs4 import BeautifulSoup
from urllib.request import urlopen
import re, requests

# 0 --> user, 1 --> repo, 2 --> filename.py
# we assume branch is master
GHRAW = "https://raw.githubusercontent.com/{0}/{1}/master/{2}"
GHREGEX1 = "^https://github.com/(.+?)/(.+?)/$"
GHREGEXERR = "^https://github.com/(.+?)/(.+?)/.+$"
GHREGEX2 = "^https://github.com/(.+?)/(.+?)$"

def _parse_link(gh_link):
    m = re.search(GHREGEX1, gh_link)

    if m is None:
        m = re.search(GHREGEXERR, gh_link)
        if m is not None:
            return None, None
        m = re.search(GHREGEX2, gh_link)
        if m is None:
            return None, None

    return m.group(1), m.group(2)

def _is_py(filename):
    return len(filename) > 3 and filename[-3:] == ".py"

def get_filemap(gh_link):

    user, repo = _parse_link(gh_link)
    print(user, repo)
    if user is None or repo is None:
        return # TODO do some sort of error handling here

    getrawgh = lambda pyfile: GHRAW.format(user, repo, pyfile)

    page = urlopen(gh_link)
    soup = BeautifulSoup(page, 'html.parser')

    filerows = soup.find_all("tr", "js-navigation-item")

    filenames = []
    for row in filerows:
        filename = row.find("a").contents[0]
        filenames.append(filename)

    pyfiles = []
    for filename in filenames:
        if _is_py(filename):
            pyfiles.append(filename)

    filemap = {}
    for pyfile in pyfiles:
        link = getrawgh(pyfile)
        filemap[pyfile] = requests.get(link).content

    return filemap
