import os

def find_file_in_directories(target_name):
  """
  Searches for applications with the given name in specific directories.

  Args:
      target_name: The name of the application to search for (e.g., "Github Desktop").

  Returns:
      A list of paths to matching applications, or an empty list if no matches are found.
  """

  # Allow search without the ".app" extension
  target_name = target_name+".app"

  # Consider expanding or customizing directories based on OS
  directories = ['/Applications', '/System/Applications']
  matching_files = []

  for directory in directories:
    if os.path.exists(directory):
      for root, dirs, files in os.walk(directory):
        for file in dirs:
          # Case-insensitive search with option for case-sensitive matching
          if file.lower() == target_name.lower() or file == target_name:
            matching_files.append(os.path.join(root, file))

  return matching_files

def jaccard_distance(set1: set, set2: set) -> float:
  # Symmetric difference of two sets
  symmetric_difference = set1.symmetric_difference(set2)
  # Unions of two sets
  union = set1.union(set2)
  # print(len(union), len(symmetric_difference))
  return float(len(union)) / float(len(symmetric_difference))