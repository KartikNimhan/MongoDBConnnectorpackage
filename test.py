from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """Reads a requirements file and returns a list of requirements without '-e .'."""
    requirements = []
    with open(file_path, 'r') as f:
        requirements = f.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]  # Strip and filter out empty lines
        
        # Remove '-e .' if present
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

# Test the function
print(get_requirements("./requirements.txt"))
