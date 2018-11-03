from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re, requests

# 0 --> user, 1 --> repo, 2 --> filename.py
# we assume branch is master
GH = "https://github.com/{0}/{1}/"
GHRAW = "https://raw.githubusercontent.com/{0}/{1}/master/{2}"
GHREGEX1 = "^.*?https://github.com/(.+?)/(.+?)/(\s*?$|\s+?-g=(.*?)\s*?$)"
GHREGEX2 = "^.*?https://github.com/(.+?)/(.+?)(\s*?$|\s+?-g=(.*?)\s*?$)"
# GHREGEXERR = "^.*?https://github.com/(.+?)/(.+?)/.+$"

def _parse_link(gh_link):

    m = re.search(GHREGEX1, gh_link)

    if m is None:
        m = re.search(GHREGEX2, gh_link)

    assert m is not None

    return m.group(1), m.group(2), m.group(4)

def _is_py(filename):
    return len(filename) > 3 and filename[-3:] == ".py"

def get_filemap(gh_link):

    user, repo, option = _parse_link(gh_link)
    print(user, repo, option)
    assert user is not None and repo is not None
    assert option is None or str.isdigit(option)

    getrawgh = lambda pyfile: GHRAW.format(user, repo, pyfile)

    try:
        page = urlopen(GH.format(user, repo))
    except HTTPError:
        raise AssertionError

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

    if len(pyfiles) == 0:
        raise AssertionError

    filemap = {}
    for pyfile in pyfiles:
        link = getrawgh(pyfile)
        filemap[pyfile] = requests.get(link).content.decode('utf-8')

    return filemap, option
