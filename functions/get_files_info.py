import os

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, directory))

    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        lines = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir, filename)

            # is this entry a directory?
            is_dir = os.path.isdir(filepath)

            # get the size in bytes
            file_size = os.path.getsize(filepath)

            # build the line like: - name: file_size=123 bytes, is_dir=False
            line = f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            lines.append(line)

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"