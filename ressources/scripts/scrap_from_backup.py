import os
import sqlite3
from rdflib import Graph, Namespace
from rdflib.namespace import DCTERMS, FOAF, DC, OWL, RDF, RDFS, SKOS

# Define all required namespaces manually
BIBO = Namespace("http://purl.org/ontology/bibo/")
HAL = Namespace("http://data.archives-ouvertes.fr/schema/")
FABIO = Namespace("http://purl.org/spar/fabio/")
ORE = Namespace("http://www.openarchives.org/ore/terms/")

# Define database file
DB_FILE = "articles.db"
ROOT_FOLDER = r"00"  # Use raw string for Windows paths

# Connect to the database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create table with all possible fields
cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rdf_about TEXT UNIQUE,
        title TEXT,
        abstract TEXT,
        arxiv_id TEXT,
        language TEXT,
        volume TEXT,
        page_start TEXT,
        page_end TEXT,
        publication_date TEXT,
        created_date TEXT,
        modified_date TEXT,
        bibliographic_citation TEXT,
        type TEXT,
        subjects TEXT,
        topic TEXT,
        is_part_of TEXT,
        contributors TEXT,
        creators TEXT,
        same_as TEXT
    )
''')
conn.commit()

def parse_rdf(file_path):
    """Parse RDF and extract metadata."""
    g = Graph()
    
    # Manually bind namespaces that might be missing in source files
    g.bind("rdfs", RDFS)
    g.bind("skos", SKOS)
    g.bind("ore", ORE)
    g.bind("hal", HAL)
    g.bind("fabio", FABIO)
    g.bind("bibo", BIBO)

    try:
        g.parse(file_path, format="xml", handle_unused_namespaces="ignore")
    except Exception as e:
        print(f"Error parsing {file_path}: {str(e)}")
        return []

    articles_data = []
    
    # Find the first fabio:Article entity
    articles = list(g.subjects(RDF.type, FABIO.Article))
    if articles:
        article = articles[1]  # Take only the second article
        data = {
            "rdf_about": str(article),
            "title": g.value(article, DCTERMS.title),
            "abstract": g.value(article, DCTERMS.abstract),
            "arxiv_id": g.value(article, HAL.arxiv),
            "language": g.value(article, DC.language),
            "volume": g.value(article, BIBO.volume),
            "page_start": g.value(article, BIBO.pageStart),
            "page_end": g.value(article, BIBO.pageEnd),
            "publication_date": g.value(article, DCTERMS.issued),
            "created_date": g.value(article, DCTERMS.created),
            "modified_date": g.value(article, DCTERMS.modified),
            "bibliographic_citation": g.value(article, DCTERMS.bibliographicCitation),
            "type": g.value(article, DCTERMS.type),
            "subjects": ", ".join(str(s) for s in g.objects(article, DC.subject)),
            "topic": g.value(article, HAL.topic),
            "is_part_of": ", ".join(str(p) for p in g.objects(article, DCTERMS.isPartOf)),
            "contributors": "",
            "creators": ", ".join(str(c) for c in g.objects(article, DCTERMS.creator)),
            "same_as": ", ".join(str(s) for s in g.objects(article, OWL.sameAs))
        }

        # Extract contributor details
        contributors = []
        for contributor_node in g.objects(article, DCTERMS.contributor):
            name = g.value(contributor_node, FOAF.name)
            if name:
                contributors.append(str(name))
        data["contributors"] = ", ".join(contributors)

        # Convert None to empty string
        for key in data:
            data[key] = str(data[key]) if data[key] is not None else ""
            
        articles_data.append(tuple(data.values()))
    
    return articles_data

def process_files(root_folder):
    """Traverse folders and process RDF files."""
    for dirpath, _, filenames in os.walk(root_folder):
        for file in filenames:
            if file.endswith(".rdf"):
                file_path = os.path.join(dirpath, file)
                print(f"Processing {file_path}...")
                articles = parse_rdf(file_path)
                for data in articles:
                    cursor.execute('''
                        INSERT OR IGNORE INTO articles (
                            rdf_about, title, abstract, arxiv_id, language, volume,
                            page_start, page_end, publication_date, created_date,
                            modified_date, bibliographic_citation, type, subjects,
                            topic, is_part_of, contributors, creators, same_as
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', data)
                conn.commit()

# Run the script
process_files(ROOT_FOLDER)
conn.close()
print("Done! Data stored in articles.db")