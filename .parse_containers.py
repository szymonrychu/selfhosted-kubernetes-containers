#!/usr/bin/env python3

import os

import jinja2

def main():
    _template_path = os.environ.get('TEMPLATE_PATH', '.sub.gitlab-ci.yml.j2')
    _output_path = os.environ.get('OUTPUT_PATH', '.sub.gitlab-ci.yml')
    containers_list = []
    for root, dirs, files in os.walk('./'):
        for file in files: 
            if 'Dockerfile' == file:
                dockerfile_path = os.path.join(root, file)[2:]
                dockerfile_root = os.path.dirname(dockerfile_path)
                name = os.path.basename(dockerfile_root)
                if os.path.isfile(os.path.join(dockerfile_root, 'VERSION')):
                    containers_list.append({
                        'name': name, 
                        'root_path': dockerfile_root
                    })
    
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(_template_path)
    output_text = template.render(containers=containers_list)  # this is where to put args to the template renderer

    with open(_output_path, 'w') as f:
        f.write(output_text)


if __name__ == '__main__':
    main()
