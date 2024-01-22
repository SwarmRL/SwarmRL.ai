import os
import yaml
import sys

def generate_mkdocs_files(package_name, package_path, docs_path):
    api_docs = []

    for root, dirs, files in os.walk(os.path.join(package_path, package_name)):
        for name in files:
            if name.endswith('.py') and not name.startswith('__'):
                module_path = os.path.join(root, name)
                relative_path = os.path.relpath(module_path, package_path)
                module_name = relative_path.replace(os.path.sep, '.').replace('.py', '')

                doc_file = f"{docs_path}/{module_name}.md"
                with open(doc_file, 'w') as f:
                    f.write(f"# {module_name} Module API Reference\n\n")
                    f.write(f"::: {module_name}\n")

                api_docs.append({module_name: f'pages/api/{module_name}.md'})

    return api_docs

def update_mkdocs_nav(api_docs, mkdocs_config_file):
    with open(mkdocs_config_file, 'r') as file:
        mkdocs_config = yaml.safe_load(file)

    api_nav = {'API Documentation': api_docs}
    mkdocs_config['nav'] = mkdocs_config.get('nav', [])
    mkdocs_config['nav'].append(api_nav)

    with open(mkdocs_config_file, 'w') as file:
        yaml.dump(mkdocs_config, file, default_flow_style=False)

# Path configurations
package_name = 'swarmrl'  # Name of your SwarmRL package
package_path = './SwarmRL'  # Path to the root of your SwarmRL package
docs_path = './docs/pages/api'    # Path where you want to save the Markdown files
mkdocs_config_file = 'mkdocs.yml' # Path to your mkdocs.yml

# Generate markdown files and update mkdocs.yml
api_docs = generate_mkdocs_files(package_name, package_path, docs_path)
update_mkdocs_nav(api_docs, mkdocs_config_file)
