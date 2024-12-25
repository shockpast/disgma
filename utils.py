import os

def generate_tree(path, prefix=""):
  files = []
  skip_folders = {"materials", "models", "sound"}
  entries = sorted(os.listdir(path))

  for i, entry in enumerate(entries):
    if entry in skip_folders:
      continue

    is_last = i == len(entries) - 1
    current_prefix = "└── " if is_last else "├── "
    full_path = os.path.join(path, entry)

    if os.path.isdir(full_path):
      files.append(f"{prefix}{current_prefix}{entry}/")
      next_prefix = prefix + ("    " if is_last else "│   ")
      files.extend(generate_tree(full_path, next_prefix))
    else:
      files.append(f"{prefix}{current_prefix}{entry}")
  return files