import typer

from typing import Annotated
import kr8s
import os
import yaml
from jsonpath_ng import parse
from iterfzf import iterfzf
from rich import print as rprint
from rich import inspect
from datetime import datetime
# from . import helpers as he


# 
# Helpers 
# 
# # TODO: no se puede importar helpers desde main.py


def time_passed(time: str) -> str:
    time =  datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    delta = datetime.now() - time
    if delta.days:
        return f"{delta.days} d"
    elif delta.seconds // 3600:
        return f"{delta.seconds // 3600} h"
    elif delta.seconds // 60:
        return f"{delta.seconds // 60} m "
    else:
        return f"{delta.seconds} s"
    

def load_config(path: str) -> dict:
    with open(path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def get_config(config = load_config("./src/kkgepo/config.yaml")):
    return config

def dealias(alias: str, config) -> dict[str, list[str]]:
    aliases = config['resources'].keys()
    components = []
    while alias:
        for a in aliases:
            if alias.startswith(a):
                components.append(a)
                alias = alias[len(a):]
                break
        else:
            raise ValueError(f"Unknown alias: {alias}")

    return {
        'commands': [],
        'flags': [],
        'resources': [r for r in components if r in config['resources']],
    }

def get_table(resource_alias, client):
    config = get_config()
    resource_name = config['resources'][resource_alias]['value'] # get real name
    table = config['resources'][resource_alias]['columns'] 
    column_titles = [col['title'] for col in table]
    col_exprs = [col['path'] for col in table] 
    # to_dict returns Box object: https://github.com/cdgriffith/Box/wiki/Converters#dictionary
    resources = [resource for resource in client.get(resource_name, namespace='traefik')] # get resources
    # inspect(resources[0].to_dict().to_dict())
    rows = [[str(eval(expr, {'r': resource} | globals() )) for expr in col_exprs] for resource in resources] # get column values
    return [column_titles] + rows

def run_command(client, config, resources: list[str], commands: list[str], flags: list[str]) -> list[str]:
    if not resources:
        raise ValueError("No resources provided")
    if not commands:
        return get_table(resources[0], client)

def table_to_rows(data: list[list[str]]) -> list[str]:
    col_lengths = [max(len(row[i]) for row in data) for i in range(len(data[0]))]
    for i, row in enumerate(data):
        data[i] = [f"{cell:<{col_lengths[j]}}" for j, cell in enumerate(row)]
        data[i] = "   ".join(data[i])
    data[0] = data[0].upper() # Upper case for headers
    return data
    


def complete_name(incomplete: str):
    config = get_config()
    completion = [ (alias, config['resources'][alias]['value']) for alias in config['resources'] if alias.startswith(incomplete) ]
    return completion


app = typer.Typer()
@app.command()
def main(command: Annotated[ str, typer.Option(autocompletion=complete_name) ]):
    client = kr8s.api(kubeconfig=os.environ.get('KUBECONFIG'))
    config = get_config()
    command = dealias(command, config)
    data = run_command(client, config, **command)
    table = table_to_rows(data)
    for row in table:
        print(row)
    # selected = iterfzf(table, sort=False,__extra__= ['--height=13','--border', '--reverse', '--prompt=$ ', '--pointer=>', '--header-lines=1', '--color', 'header:reverse'])
    # print(selected)


if __name__ == "__main__":
    app()