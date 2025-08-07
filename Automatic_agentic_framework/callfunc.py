import openai
import os
try:
    client = openai.OpenAI(
        api_key=os.environ.get("API_KEY"),  # Recommended: Use environment variables
        # api_key=sk-C44ckypFWHqTc7xifvIOHHSsD0KeODF4QQ1OpcwnM6YAJALP
        base_url = "http://35.220.164.252:3888/v1/",
    )
except TypeError:
    print(" OpenAI API Key not found.")
    print("   Please set the OPENAI_API_KEY environment variable or hardcode it in the script.")
    exit()



system_prompt_1_en = """
You are an imaginative world architect and a technical artist. Your mission is to fuse a series of fundamental concepts provided by the user (e.g., physics, math, artistic concepts) to create a concrete, detailed, and dynamic virtual scene.

Your output must adhere to the following guidelines:
1.  **Structured Output**: Use a clear key-value format to describe the scene, making it easy to parse later.
2.  **Code-like Description**: Use precise, quantifiable language, as if writing pseudocode or a configuration file. Avoid vague, literary descriptions.
3.  **Dynamics and Interaction**: Focus on describing the behavior of elements, their interaction rules, and how they embody the user's core concepts.

Example Output Format:
Scene Name: [A creative name for the scene]
Core Concepts: [Summarize the user's concepts and how they are manifested in the scene]
Element List:
  - Element A:
    - Type: [e.g., Static Body, Dynamic Particle, Interactive Character]
    - Visual Description: [A concise description of its appearance, material, color]
    - Initial State: [Position coordinates, rotation angle, initial velocity, etc.]
    - Behavioral Rules: [Describe how it moves, changes, and embodies the core concepts]
  - Element B:
    ...
Physics & Interaction Rules:
  - Rule 1: [e.g., Global gravity is set to a vector of (0, 0.1)]
  - Rule 2: [e.g., When Element A and B collide, trigger a 'symmetrical' bounce effect]
  - Rule 3: [e.g., An element must find a path from a start to an end point, demonstrating 'pathfinding']
"""

system_prompt_2_en = """
You are a senior Python game developer and an expert in using the Pygame library. Your task is to write a single, complete, and executable Pygame program that simulates the scene, strictly following the structured scene description provided by the user.

Your code must adhere to the following guidelines:
1.  **Code Completeness**: Generate a single, complete Python script that includes all necessary Pygame initialization, the main loop, event handling, and rendering code.
2.  **Precise Implementation**: The code's logic must accurately implement every element, behavior, and physical rule from the scene description.
3.  **Readability**: The code must be clean and well-commented. Especially in the parts implementing core concepts (like gravity, pathfinding, rotation), explain how the code corresponds to the design document.
4.  **No External Assets**: Use Pygame's drawing functions (e.g., `pygame.draw`) to create geometric shapes. Do not rely on any external image or audio files.
"""

def run_generative_pipeline(concepts: str, model_name: str = "gemini2.5-pro"):
    """
    Executes a two-stage generative pipeline:
    1. Generates a structured scene description from base concepts.
    2. Generates Pygame code from the scene description.

    Args:
        concepts (str): A string of base concepts provided by the user.
        model_name (str): The name of the LLM to use.
    """
    print("="*30)
    print(" Stage 1: Generating Scene Description from Concepts")
    print(f"Input Concepts: {concepts}")
    print("="*30)
    
    try:
        # ------------------- First Prompt Call -------------------
        response_1 = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt_1_en},
                {"role": "user", "content": concepts}
            ],
            temperature=0.2 # A bit of creativity is good here
        )
        scene_description = response_1.choices[0].message.content
        
        print("\n Stage 1 Complete! Generated Scene Description:\n")
        print(scene_description)
        print("\n" + "="*30)
        
        # ------------------- Second Prompt Call -------------------
        print(" Stage 2: Generating Pygame Code from Scene Description")
        print("="*30)
        
        response_2 = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_prompt_2_en},
                # The output of the first call is the input for the second
                {"role": "user", "content": scene_description} 
            ],
            temperature=0 # Code generation needs to be precise
        )
        generated_code = response_2.choices[0].message.content
        
        print("\n Stage 2 Complete! Generated Pygame Code:\n")
        # Clean up the markdown code block formatting
        if "```python" in generated_code:
            generated_code = generated_code.split("```python\n", 1)[1].rsplit("```", 1)[0]
            
        print(generated_code)

        # Save the code to a file
        output_filename = "generated_scene.py"
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(generated_code)
        print(f"  Task Complete! Code has been saved to `{output_filename}`.")
        print(f"   You may need to install pygame (`pip install pygame`) to run it.")
        print(f"   To run the code, execute: `python {output_filename}`")

    except openai.APIConnectionError as e:
        print(" Connection Error: Could not connect to the API. Please check your network and Base URL.")
        print(f"   Details: {e.__cause__}")
    except openai.AuthenticationError as e:
        print(" Authentication Error: The API Key is incorrect or has expired. Please check your API Key.")
    except openai.RateLimitError as e:
        print(" Rate Limit Error: You have hit the API's rate limit. Please wait and try again.")
    except Exception as e:
        print(f" An unexpected error occurred: {e}")


if __name__ == "__main__":
    base_concepts = "Symmetry, Pathfinding, Gravity, Rotation"
    run_generative_pipeline(base_concepts)