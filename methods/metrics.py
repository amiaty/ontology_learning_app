def calculate_metrics(ref_ontology_path=None, gen_ontology_path=None, ref_content=None, gen_content=None):
    """
    Calculate evaluation metrics between reference and generated ontologies.
    Can work with either file paths or content strings.
    
    Args:
        ref_ontology_path: Path to reference ontology TTL file
        gen_ontology_path: Path to generated ontology TTL file
        ref_content: String content of reference ontology
        gen_content: String content of generated ontology
        
    Returns:
        Dictionary of metrics
    """
    import tempfile
    import os
    from rdflib import Graph
    
    # Create temporary files if content strings are provided
    temp_files = []
    
    if ref_content and not ref_ontology_path:
        temp_ref = tempfile.NamedTemporaryFile(delete=False, suffix='.ttl')
        temp_ref.write(ref_content.encode('utf-8'))
        temp_ref.close()
        ref_ontology_path = temp_ref.name
        temp_files.append(ref_ontology_path)
    
    if gen_content and not gen_ontology_path:
        temp_gen = tempfile.NamedTemporaryFile(delete=False, suffix='.ttl')
        temp_gen.write(gen_content.encode('utf-8'))
        temp_gen.close()
        gen_ontology_path = temp_gen.name
        temp_files.append(gen_ontology_path)
    
    # Load the ontologies
    ref_graph = Graph()
    gen_graph = Graph()
    
    try:
        ref_graph.parse(ref_ontology_path, format="turtle")
        gen_graph.parse(gen_ontology_path, format="turtle")
    except Exception as e:
        # Clean up temp files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        raise Exception(f"Error parsing ontology: {str(e)}")
    
    # Namespace prefixes for RDF, RDFS, OWL
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    rdfs = "http://www.w3.org/2000/01/rdf-schema#"
    owl = "http://www.w3.org/2002/07/owl#"
    
    # Query to get classes
    class_query = f"""
    SELECT DISTINCT ?class WHERE {{
        ?class a <{owl}Class> .
        FILTER(?class != <{owl}Thing> && ?class != <{owl}Nothing>)
    }}
    """
    
    # Query to get object properties
    obj_prop_query = f"""
    SELECT DISTINCT ?prop WHERE {{
        ?prop a <{owl}ObjectProperty> .
    }}
    """
    
    # Query to get data properties
    data_prop_query = f"""
    SELECT DISTINCT ?prop WHERE {{
        ?prop a <{owl}DatatypeProperty> .
    }}
    """
    
    # Query to get individuals
    individual_query = f"""
    SELECT DISTINCT ?individual WHERE {{
        ?individual a ?type .
        FILTER(?type != <{owl}Class> && ?type != <{owl}ObjectProperty> && 
               ?type != <{owl}DatatypeProperty> && ?type != <{rdfs}Class> &&
               ?type != <{rdf}Property>)
    }}
    """
    
    # Get all elements from both graphs
    ref_classes = set(result["class"] for result in ref_graph.query(class_query))
    gen_classes = set(result["class"] for result in gen_graph.query(class_query))
    
    ref_obj_props = set(result["prop"] for result in ref_graph.query(obj_prop_query))
    gen_obj_props = set(result["prop"] for result in gen_graph.query(obj_prop_query))
    
    ref_data_props = set(result["prop"] for result in ref_graph.query(data_prop_query))
    gen_data_props = set(result["prop"] for result in gen_graph.query(data_prop_query))
    
    ref_individuals = set(result["individual"] for result in ref_graph.query(individual_query))
    gen_individuals = set(result["individual"] for result in gen_graph.query(individual_query))
    
    # Find common elements
    common_classes = ref_classes.intersection(gen_classes)
    common_obj_props = ref_obj_props.intersection(gen_obj_props)
    common_data_props = ref_data_props.intersection(gen_data_props)
    common_individuals = ref_individuals.intersection(gen_individuals)
    
    # Get axiom counts
    ref_axioms = len(list(ref_graph))
    gen_axioms = len(list(gen_graph))
    
    # Approximate common axioms by comparing triples
    common_axioms = sum(1 for triple in gen_graph if triple in ref_graph)
    
    # Get logical axiom counts (approximation - actual calculation would require OWL API)
    ref_logical_axioms = ref_axioms - len(ref_classes) - len(ref_obj_props) - len(ref_data_props)
    gen_logical_axioms = gen_axioms - len(gen_classes) - len(gen_obj_props) - len(gen_data_props)
    common_logical_axioms = common_axioms - len(common_classes) - len(common_obj_props) - len(common_data_props)
    
    # Calculate metrics
    # Completeness: What percentage of the reference ontology is covered
    if len(ref_classes) + len(ref_obj_props) + len(ref_data_props) + len(ref_individuals) > 0:
        completeness = (len(common_classes) + len(common_obj_props) + len(common_data_props) + len(common_individuals)) / \
                      (len(ref_classes) + len(ref_obj_props) + len(ref_data_props) + len(ref_individuals))
    else:
        completeness = 0
    
    # Conciseness: What percentage of the generated ontology is relevant
    if len(gen_classes) + len(gen_obj_props) + len(gen_data_props) + len(gen_individuals) > 0:
        conciseness = (len(common_classes) + len(common_obj_props) + len(common_data_props) + len(common_individuals)) / \
                     (len(gen_classes) + len(gen_obj_props) + len(gen_data_props) + len(gen_individuals))
    else:
        conciseness = 0
    
    # Correctness: Harmonic mean of completeness and conciseness
    if completeness + conciseness > 0:
        correctness = 2 * (completeness * conciseness) / (completeness + conciseness)
    else:
        correctness = 0
    
    # Clean up temp files
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    # Return all metrics
    return {
        'completeness': completeness,
        'conciseness': conciseness,
        'correctness': correctness,
        'ref_classes': len(ref_classes),
        'gen_classes': len(gen_classes),
        'common_classes': len(common_classes),
        'ref_obj_props': len(ref_obj_props),
        'gen_obj_props': len(gen_obj_props),
        'common_obj_props': len(common_obj_props),
        'ref_data_props': len(ref_data_props),
        'gen_data_props': len(gen_data_props),
        'common_data_props': len(common_data_props),
        'ref_individuals': len(ref_individuals),
        'gen_individuals': len(gen_individuals),
        'common_individuals': len(common_individuals),
        'ref_axioms': ref_axioms,
        'gen_axioms': gen_axioms,
        'common_axioms': common_axioms,
        'ref_logical_axioms': ref_logical_axioms,
        'gen_logical_axioms': gen_logical_axioms,
        'common_logical_axioms': common_logical_axioms
    }