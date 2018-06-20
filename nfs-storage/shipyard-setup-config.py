"""
Setup the YAML configuration files to be used with Batch Shipyard.
"""

import pathlib
import argparse
import subprocess


def parse_command_line():
  """
  Parses the command-line options.
  """
  formatter_class = argparse.ArgumentDefaultsHelpFormatter
  description = 'Batch Shipyard: setup the configuration files.'
  parser = argparse.ArgumentParser(description=description,
                                   formatter_class=formatter_class)
  parser.add_argument('--version', '-V',
                      action='version',
                      version='%(prog)s (version 0.1)')
  parser.add_argument('--configdir', dest='config_dir',
                      type=str,
                      required=True,
                      help='Directory with all configuration files.')
  parser.add_argument('--resource-group', dest='resource_group',
                      type=str,
                      required=True,
                      help='Name of resource group.')
  parser.add_argument('--account-name', dest='account_name',
                      type=str,
                      required=True,
                      help='Storage account name.')
  args = parser.parse_args()
  return args


def get_storage_account_key(resource_group, account_name):
  cmd_str = ('az storage account keys list'
             '--resource-group {} --account-name {} '
             '--output json --query "[0].value"'
             .format(resource_group, account_name))
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return output


def main(args):
  data = {}


if __name__ == '__main__':
  args = parse_command_line()
  main(args)
