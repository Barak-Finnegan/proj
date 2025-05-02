#!/usr/bin/env python3

import argparse
import subprocess
import venv
import os

parser = argparse.ArgumentParser(
        prog='proj',
        description='This is a helper program for project maintenance and synthesis',
    )

subparsers = parser.add_subparsers(description='valid subcommands of proj', required=True, help='sub-command help')
    
def run(args):
    commands = args.commands
    if not commands:
        commands = ['python3']
    else:
        commands = ['python3'] + commands
    subprocess.run(['./.bash/run'] + commands)

def install(args):
    subprocess.run(['./.bash/run', 'python3',
                    '-m', 'pip', 'install'] + args.packages)

def remove(args):
    subprocess.run(['./.bash/run', 'python3',
                    '-m', 'pip', 'uninstall', '-y'] + args.packages)

def packages(args):
    subprocess.run(['./.bash/run', 'python3',
                    '-m', 'pip', 'freeze'])

def create(args):
    os.mkdir(args.name)
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(args.name)
    os.mkdir(f'{args.name}/.bash')
    os.mkdir(f'{args.name}/{args.name}')
    with open(f'{args.name}/.bash/run', 'w') as f:
        f.write('#!/bin/bash\n' +
                'source bin/activate\n' +
                '$@\n')
    subprocess.run(['chmod', '+x', f'{args.name}/.bash/run'])
    subprocess.run(['touch', f'{args.name}/{args.name}/__init__.py'])
    subprocess.run(['touch', f'{args.name}/{args.name}/__main__.py'])

def compile(args):
    if not os.path.exists('./build'):
        os.mkdir('build')

    if args.add_to_path:
        print(args.add_to_path)

run_parser = subparsers.add_parser('run', help='runs the project')
run_parser.add_argument('commands', nargs='*')
run_parser.set_defaults(func=run)
create_parser = subparsers.add_parser('create', help='creates a new project')
create_parser.add_argument('name')
create_parser.set_defaults(func=create)
compile_parser = subparsers.add_parser('compile', help='compile the project to a binary')
compile_parser.add_argument('--add-to-path', action='store_true')
compile_parser.set_defaults(func=compile)
install_parser = subparsers.add_parser('install', help='can be used to add third party dependencies')
install_parser.add_argument('packages', nargs='*')
install_parser.set_defaults(func=install)
remove_parser = subparsers.add_parser('remove', help='can be used to remove third party dependencies')
remove_parser.add_argument('packages', nargs='*')
remove_parser.set_defaults(func=remove)
packages_parser = subparsers.add_parser('packages', help='show all third party packages of the environment').set_defaults(func=packages)

args = parser.parse_args()
args.func(args)
