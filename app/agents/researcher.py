import requests
import xml.etree.ElementTree as ET
from app.utils.config import ARXIV_API_URL

def fetch_arxiv_papers(query, max_results=15):
    url = f"{ARXIV_API_URL}?search_query=all:{query}&start=0&max_results={max_results}"
    
    response = requests.get(url)
    root = ET.fromstring(response.content)

    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        
        papers.append({
            "title": title,
            "summary": summary,
            "year": None,
            "citations": 0,
            "authors": [],
            "url": "",
            "source": "arxiv",
            "link": entry.find("{http://www.w3.org/2005/Atom}id").text
        })


    return papers
