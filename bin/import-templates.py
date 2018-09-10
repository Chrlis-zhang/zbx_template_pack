#!/usr/bin/env python
import argparse
import json
import os
from zabbix.api import ZabbixAPI
import zabbix_cli

def import_configuration_from_file(zapi, filename):
    """This imports configuration into ZabbixAPI from file"""
    with open(filename, 'r') as file:
        contents = file.read()
    params_raw = """
    {
        "format": "xml",
        "rules": {
            "groups": {
                "createMissing": true
            },
            "hosts": {
                "createMissing": true,
                "updateExisting": true
            },
            "templates": {
                "createMissing": true,
                "updateExisting": true
            },            
            "templateLinkage": {
                "createMissing": true
            },                    
            "templateScreens": {
                "createMissing": true,
                "updateExisting": true,
                "deleteMissing": true
            },   
            "applications": {
                "createMissing": true,
                "deleteMissing": true
            },    
            "discoveryRules": {
                "createMissing": true,
                "updateExisting": true,
                "deleteMissing": true
            },            
            "items": {
                "createMissing": true,
                "updateExisting": true,
                "deleteMissing": true
            },
            "triggers": {
                "createMissing": true,
                "updateExisting": true,
                "deleteMissing": true
            },
            "graphs": {
                "createMissing": true,
                "updateExisting": true,
                "deleteMissing": true
            },
            "screens": {
                "createMissing": true,
                "updateExisting": true
            },
            "maps": {
                "createMissing": true,
                "updateExisting": true
            },
            "images": {
                "createMissing": true,
                "updateExisting": true
            },
            "valueMaps": {
                "createMissing": true,
                "updateExisting": true
            }
        },
        "source": ""
        }
    """
    params = json.loads(params_raw)
    params['source'] = contents
    zapi.do_request('configuration.import', params)


def import_single_template(filename):
    """This imports single template"""
    print ("Importing {}...".format(filename))
    import_configuration_from_file(zapi, filename)


def import_dir_with_templates(dirname):
    """This imports all templates found in the directory"""
    import glob

    templates = []
    for file in glob.glob(dirname+'/*'+args.filter_str+"*.xml"):
        templates.append(file)
    if len(templates) == 0:
        print("No templates found in directory {} with filter: {}".format(
            dirname, args.filter_str))
    templates.sort()
    for template in templates:
        import_single_template(template)




template_parser = zabbix_cli.zabbix_default_args()
parser = argparse.ArgumentParser(parents=[template_parser], add_help=False)
parser.add_argument('--filter', '-f', dest='filter_str',
                    help="Imports only files that contain filter specified in their filenames.",
                    required=False, type=str, default='')
parser.add_argument(dest='arg1', nargs=1, help='filename|dirname')
args = parser.parse_args()

zapi = ZabbixAPI(url=args.api_url,
                 user=args.username,
                 password=args.password)

if os.path.isdir(args.arg1[0]):
    import_dir_with_templates(args.arg1[0])
elif os.path.isfile(args.arg1[0]):
    import_single_template(args.arg1[0])

zapi.do_request('user.logout')
