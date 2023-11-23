#!/usr/bin/env python3

import argparse
import glob
import jinja2
import logging
import os
import yaml

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Jinja util to template things e.g. for configuration in helm chart')
parser.add_argument('-v','--values', nargs='+', help='List of YAML files with K/V values for the templates', required=False)
parser.add_argument('-t','--templates-dir', help='Directory where all templates are located', required=True)
parser.add_argument('-o', '--output-dir', help='Output path', required=True, type=str)
parser.add_argument('--env-prefix', default='JINJA_', help='Prefix for the env variables', required=False, type=str)
parser.add_argument('-f', '--replace-files', help='Replace output file if exists', action='store_true', default=False)

args = vars(parser.parse_args())

template_files_root = os.path.abspath(args['templates_dir'])

templates_files = []
templates_glob = os.path.join(template_files_root, '**', '*.jinja2')
for fpath in glob.glob(templates_glob, recursive=True):
    templates_files.append(os.path.abspath(fpath))

values_files = []
for value_file_glob in args['values']:
    for fpath in glob.glob(value_file_glob):
        values_files.append(os.path.abspath(fpath))

values = {}
for fpath in values_files:
    yaml_data = None
    with open(fpath) as f:
        yaml_data = yaml.safe_load(f)

    fname_wo_ext = '.'.join(os.path.basename(fpath).split('.')[:-1])

    if yaml_data:
        logging.info(f"Loaded values from '{fpath}'")
        values[fname_wo_ext] = yaml_data

env_values = {}
for env_name, env_value in dict(os.environ).items():
    if env_name.startswith(args['env_prefix']):
        sanitized_env_name = env_name[len(args['env_prefix']):].lower()
        env_values[sanitized_env_name] = env_value

if env_values:
    logging.info('Loaded additional values from env')
    values['env'] = env_values


for template_file in templates_files:
    template_contents = None
    with open(template_file) as f:
        template_contents = f.read()
    
    if not template_contents:
        continue

    logging.info(f"Loaded template '{template_file}'")

    environment = jinja2.Environment()
    template = environment.from_string(template_contents)
    output = template.render(values)
    
    relative_template_path = os.path.relpath(template_file, template_files_root)
    output_path = '.'.join(os.path.join(args['output_dir'], relative_template_path).split('.')[:-1])
    if not args['replace_files'] and os.path.exists(output_path):
        logging.info(f"Ommiting output file '{output_path}', as it already exists!")
        continue 

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Created directory '{output_dir}'")

    with open(output_path, 'w') as f:
        f.write(output)

    logging.info(f"Written output file '{output_path}'")

