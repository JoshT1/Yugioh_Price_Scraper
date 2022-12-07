from urllib.request import urlopen
import xml.etree.ElementTree as ET


# Read card map XML file and put every product card ID into a list iteratively.
def xml_parser(url):
    with urlopen(url) as f:
        tree = ET.parse(f)
        root = tree.getroot()

    i = 0
    list_id = []
    while i < root.__len__():
        cur = root[i][0].text
        if cur.startswith('https://www.tcgplayer.com/product/'):
            cur_list = cur.split("/")
            list_id.append(cur_list[4])
        i += 1
    return list_id
