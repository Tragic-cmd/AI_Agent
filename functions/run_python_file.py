import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Used to execute python files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):

    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))

    prefix = abs_working_dir + os.sep
    if not (target_dir == abs_working_dir or target_dir.startswith(prefix)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    file_type_extension = '.py'

    if not file_path.endswith(file_type_extension):
        return f'Error: "{file_path}" is not a Python file.'
    
    if not os.path.isfile(target_dir):
        return f'Error: File "{file_path}" not found.'


    try:

        completed = subprocess.run(
            ["python", file_path, *args],
            cwd=working_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            text=True,
        )

        if not (completed.stdout or completed.stderr):
            return "No output produced"
    
        result = f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}"

        if completed.returncode != 0:
            result += f"\nProcess exited with code {completed.returncode}"

        return result


    except Exception as e:
        return f"Error: executing Python file: {e}"
