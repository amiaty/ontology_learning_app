def text_to_llm_prompt(description: str) -> list[dict[str, str]]:
    """
    Generate a ChatGPT prompt for creating an OWL ontology from a text description.

    Parameters
    ----------
    description: str
        The input text describing the ontology.

    Returns
    -------
    list[dict[str, str]]
        A prompt formatted for ChatGPT.
    """
    prompt = [
        {
            "role": "system",
            "content": "You are an expert ontology engineer specialized in converting domain texts into formal OWL ontologies. You have deep expertise in knowledge representation, semantic web technologies (RDF, RDFS, OWL), and ontology design patterns. Your task is to create precise, well-structured ontologies that accurately capture the semantics of the provided text.",
        },
        {
            "role": "user",
            "content": "Use the given text to construct an OWL ontology in the Turtle format. Use this namespace: https://bim-connected.com/genai#. Return ONLY valid Turtle syntax as plain text without ANY formatting, backticks, or language tags.",
        },
        {
            "role": "user",
            "content": f"Text:\n{description}",
        },
    ]
    return prompt

def create_ontology_from_description(description: str, model="gpt-4o") -> str:
    """
    Generate an ontology from text using LLM.
    
    Args:
        text: The text content to process
        model: The OpenAI model to use (gpt4, gpt4omini)
        
    Returns:
        TTL formatted ontology as string
    """
    import openai
    import os
    
    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is required. Set it in the environment variable OPENAI_API_KEY.")
    openai.api_key = api_key
    client = openai.OpenAI(api_key=api_key)

    # Create the prompt using the description
    prompt = text_to_llm_prompt(description)

    # Request response from GPT model
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=prompt,
    )
    llm_output = response.choices[0].message.content
    
    return llm_output

def create_ontology_from_description2(description: str, model="gpt-4o") -> str:
    """
    Generate an ontology from text using LLM.
    
    Args:
        text: The text content to process
        model: The OpenAI model to use (gpt4, gpt4omini)
        
    Returns:
        TTL formatted ontology as string
    """
    import openai
    import os
    
    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is required. Set it in the environment variable OPENAI_API_KEY.")
    openai.api_key = api_key
    client = openai.OpenAI(api_key=api_key)

    # Create the prompt using the description
    prompt = text_to_llm_prompt(description)

    # Request response from GPT model
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=prompt,
    )
    llm_output = response.choices[0].message.content
    
    return llm_output

def generate_ontology_from_text(text, model="gpt4"):
    """
    Generate an ontology from text using LLM.
    
    Args:
        text: The text content to process
        model: The OpenAI model to use (gpt4, gpt4omini)
        
    Returns:
        TTL formatted ontology as string
    """
    import openai
    import os
    import re
    
    # Get API key from environment
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key is required. Set it in the environment variable OPENAI_API_KEY.")
    
    openai.api_key = api_key
    
    # Determine which model to use
    if model == "gpt4":
        model_name = "gpt-4"
    elif model == "gpt4omini":
        model_name = "gpt-4o-mini"
    else:
        model_name = "gpt-4"  # Default to GPT-4
    
    # Construct the prompt
    prompt = f"""
    You are an expert in ontology engineering and semantic web. You will generate an OWL ontology from the given text.
    
    The ontology should be formatted in Turtle (TTL) syntax and follow these guidelines:
    1. Extract relevant classes, properties, and instances from the text
    2. Create proper class hierarchies
    3. Define object properties and data properties
    4. Add domain and range restrictions
    5. Include annotations for documentation
    6. Add logical axioms where appropriate
    
    Here is the text to process:
    ```
    {text}
    ```
    
    Please generate a complete OWL ontology in Turtle format with appropriate namespaces.
    """
    
    try:
        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert in ontology engineering and knowledge representation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=4000
        )
        
        # Extract the ontology text
        ontology_text = response.choices[0].message.content
        
        # Clean up the response to remove markdown code blocks
        ontology_text = re.sub(r'```turtle|```ttl|```', '', ontology_text)
        ontology_text = ontology_text.strip()
        
        return ontology_text
        
    except Exception as e:
        raise Exception(f"Error generating ontology: {str(e)}")