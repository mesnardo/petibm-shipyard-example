#!/usr/bin/env python
"""
Setup the YAML configuration files to be used with Batch Shipyard.
"""

import os
import argparse
import subprocess
import ast


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
  cmd_str = ('az storage account keys list '
             '--resource-group {} --account-name {} '
             '--output json --query "[0].value"'
             .format(resource_group, account_name))
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return ast.literal_eval(output)


def get_resource_group_location(resource_group):
  cmd_str = ('az group show '
             '--resource-group {} '
             '--output json --query "location"'
             .format(resource_group))
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return ast.literal_eval(output)


def get_subscription_ids():
  cmd_str = ('az account show --output json --query "[id, tenantId]"')
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return ast.literal_eval(output)


def get_username():
  cmd_str = ('az account show --output json --query "user.name"')
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return ast.literal_eval(output)


def get_batch_account_name(resource_group):
  cmd_str = ('az batch account list '
             '--resource-group {} '
             '--output json --query "[0].name"'
             .format(resource_group))
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return ast.literal_eval(output)


def get_batch_account_endpoint(resource_group):
  cmd_str = ('az batch account list '
             '--resource-group {} '
             '--output json --query "[0].accountEndpoint"'
             .format(resource_group))
  output = subprocess.check_output(cmd_str, shell=True).decode('ascii')
  return ast.literal_eval(output)


def get_config_paths(config_dir):
  if os.path.isdir(config_dir):
    filenames = ['config.yaml', 'credentials.yaml', 'fs.yaml',
                 'pool.yaml', 'jobs.yaml']
    return [os.path.join(config_dir, name) for name in filenames]


def replace_strings_in_files(filepaths, info):
  for path in filepaths:
    with open(path, 'r') as infile:
      lines = infile.readlines()
    for i, line in enumerate(lines):
      for key, value in info.items():
        if key in line:
          lines[i] = line.replace(key, value)
    with open(path, 'w') as outfile:
      outfile.writelines(lines)


def main(args):
  info = {}
  info['<resource-group>'] = args.resource_group
  info['<storage-account-name>'] = args.account_name
  info['<storage-account-key>'] = get_storage_account_key(args.resource_group,
                                                          args.account_name)
  info['<location>'] = get_resource_group_location(args.resource_group)
  info['<subscription-id>'], info['<tenant-id>'] = get_subscription_ids()
  info['<username>'] = get_username()
  info['<batch-account-name>'] = get_batch_account_name(args.resource_group)
  url = 'https://' + get_batch_account_endpoint(args.resource_group)
  info['<batch-account-service-url>'] = url
  configpaths = get_config_paths(args.config_dir)
  replace_strings_in_files(configpaths, info)


if __name__ == '__main__':
  args = parse_command_line()
  main(args)
