# metrics.py
import rdflib

def normalize_term(term):
    """
    Normalize RDF terms for easier comparison.
    
    Parameters:
        term: An RDFLib term (URIRef, Literal, or BNode)
    
    Returns:
        str: Lowercase string representation of the term
    """
    if isinstance(term, rdflib.URIRef):
        term_str = str(term)
        return term_str.split('#')[-1].lower() if '#' in term_str else term_str.split('/')[-1].lower()
    elif isinstance(term, rdflib.Literal):
        return str(term).lower()
    elif isinstance(term, rdflib.BNode):
        return "bnode"
    return str(term).lower()

def load_and_normalize(file_path: str) -> set:
    """
    Load a Turtle RDF graph and normalize its triples.

    Parameters:
        file_path (str): Path to the RDF Turtle file.

    Returns:
        set: Set of normalized triples as tuples (subject, predicate, object).
    """
    graph = rdflib.Graph()
    graph.parse(file_path, format="turtle")
    return {(normalize_term(s), normalize_term(p), normalize_term(o)) for s, p, o in graph}

def conciseness(learned: set, reference: set) -> float:
    """
    Compute conciseness score as intersection ratio with learned ontology.

    Parameters:
        learned (set): Set of triples from learned ontology.
        reference (set): Set of triples from reference ontology.
    
    Returns:
        float: Conciseness score.
    """
    return len(learned.intersection(reference)) / len(learned) if learned else 0.0

def completeness(learned: set, reference: set) -> float:
    """
    Compute completeness score as intersection ratio with reference ontology.

    Parameters:
        learned (set): Set of triples from learned ontology.
        reference (set): Set of triples from reference ontology.
    
    Returns:
        float: Completeness score.
    """
    return len(learned.intersection(reference)) / len(reference) if reference else 0.0

def correctness(learned: set, reference: set) -> float:
    """
    Compute correctness as harmonic mean of conciseness and completeness.

    Parameters:
        learned (set): Set of triples from learned ontology.
        reference (set): Set of triples from reference ontology.
    
    Returns:
        float: Correctness score.
    """
    conc = conciseness(learned, reference)
    comp = completeness(learned, reference)
    return 2 * (conc * comp) / (conc + comp) if conc + comp else 0.0
