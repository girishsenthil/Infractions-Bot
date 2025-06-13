import os
import sys
import importlib.util

# Add 'src' to the module search path
SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, SRC_DIR)

print(f"Checking imports in: {SRC_DIR}")
failures = []

# Walk through all Python files under 'src'
for root, _, files in os.walk(SRC_DIR):
    for filename in files:
        if filename.endswith('.py'):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, SRC_DIR)
            module_path = rel_path.replace('/', '.').replace('\\', '.').removesuffix('.py')

            # Skip __main__.py or similar files if needed
            if module_path.endswith('__main__'):
                continue

            try:
                importlib.import_module(module_path)
                print(f"✅ {module_path}")
            except Exception as e:
                print(f"❌ {module_path} failed to import: {e}")
                failures.append((module_path, str(e)))

# Final result
if failures:
    print("\n--- Import Errors ---")
    for mod, err in failures:
        print(f"{mod}: {err}")
    exit(1)
else:
    print("\n✅ All modules imported successfully.")
