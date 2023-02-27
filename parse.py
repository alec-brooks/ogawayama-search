from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
import json

def parse_doc(doc, page_name):
    sep = '<a name'
    page_chunks = [sep+x for x in doc.split(sep)[1:]]

    return flatten([parse_anchor_chunk(p, page_name) for p in page_chunks])

def parse_anchor_chunk(doc, page_name):
    soup = BeautifulSoup(doc, 'html.parser')
    anchor_name = [x.get('name') for x in soup.find_all('a') if x is not None][0]
    climb_description_tables = soup.find_all("table")
    return [parse_climb_table(ct, anchor_name, page_name) for ct in climb_description_tables]

@dataclass(unsafe_hash=True)
class ClimbTable:
    link: str
    title: str
    grade: str
    quality: int
    height: float
    description: str
    notes: str

def parse_climb_table(climb_table, anchor_name, page_name):
    tds = climb_table.find_all('td')
    if len(tds) not in [4,5,6]:
        return None
    title = tds[0].get_text().strip()
    grade = tds[1].get_text().rstrip('*').strip()
    if not grade.startswith("5."):
        return None
    quality = tds[1].get_text().count('*')
    height = float(tds[2].get_text().rstrip('m'))
    description = tds[3].get_text().strip().replace('\n', '').replace('"', '\"')
    notes = tds[4].get_text().strip().replace('\n', '').replace('"', '\"') if len(tds)>4 else ''

    link = f"https://ogawayama.online/{page_name}.html#{anchor_name}"
    return ClimbTable(
        link, 
        title,
        grade,
        quality,
        height,
        description,
        notes,
    )

def flatten(l):
    return [item for sublist in l for item in sublist]


if __name__ == "__main__":
    html_files = [
            "camp",
            "bagashit",
            "eboshi",
            "family",
            "gamma",
            "godzilla",
            "karasawa",
            "sagan",
            "waterfall",
            "yanes",
            ]
    climbing_tables = []
    for f in html_files:
        doc = open(f"pages/{f}.html","r", errors="ignore").read()
        climbing_tables.append(parse_doc(doc, f))
    filtered_cts = [x for x in flatten(climbing_tables) if x is not None]

    ndjson_cts = '\n'.join([json.dumps(asdict(ct)) for ct in filtered_cts])
    print(ndjson_cts)


