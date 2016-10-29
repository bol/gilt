# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2016 Cisco Systems, Inc.
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to
#  deal in the Software without restriction, including without limitation the
#  rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.

import os

import click

import gilt
from gilt import config
from gilt import git
from gilt import util


class NotFoundError(Exception):
    """ Error raised when a config can not be found. """
    pass


def main():
    """ gilt - A GIT layering tool. """
    cli(obj={})


@click.group()
@click.option(
    '--config',
    default='gilt.yml',
    help='Path to config file.  Default gilt.yml')
@click.option(
    '--debug/--no-debug',
    default=False,
    help='Enable or disable debug mode. Default is disabled.')
@click.version_option(version=gilt.__version__)
@click.pass_context
def cli(ctx, config, debug):  # pragma: no cover
    ctx.obj['args'] = {}
    ctx.obj['args']['debug'] = debug
    ctx.obj['args']['config'] = config


@click.command()
@click.pass_context
def overlay(ctx):  # pragma: no cover
    """ Install gilt dependencies """
    args = ctx.obj.get('args')
    filename = args.get('config')
    debug = args.get('debug')
    _setup(filename)

    for c in config.config(filename):
        util.print_info('{}:'.format(c.name))
        if not os.path.exists(c.src):
            git.clone(c.name, c.git, c.src, debug=debug)
        if c.dst:
            git.extract(c.src, c.dst, c.version, debug=debug)
        else:
            git.overlay(c.src, c.files, c.version, debug=debug)


def _setup(filename):
    if not os.path.exists(filename):
        msg = 'Unable to find {}. Exiting.'.format(filename)
        raise NotFoundError(msg)

    d = config._get_clone_dir()
    if not os.path.exists(d):
        os.makedirs(d)


cli.add_command(overlay)