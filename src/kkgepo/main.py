import typer
import kr8s
import os
import yaml
from jsonpath_ng import parse
from iterfzf import iterfzf
from rich import print as rprint
from rich import inspect

def load_config(path: str) -> dict:
    with open(path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

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


def run_command(client, config, resources: list[str], commands: list[str], flags: list[str]) -> list[str]:
    if not resources:
        raise ValueError("No resources provided")
    if not commands:
        resource_alias = resources[0]
        resource_name = config['resources'][resource_alias]['value']
        table = config['resources'][resource_alias]['columns']
        column_titles = [col['title'] for col in table]
        # col_exprs = [parse(col['path']) for col in table] 
        col_exprs = [col['path'] for col in table] 

        # to_dict returns Box object: https://github.com/cdgriffith/Box/wiki/Converters#dictionary
        resources = [resource for resource in client.get(resource_name, namespace='traefik')]
        inspect(resources[0].to_dict().to_dict())
        print(col_exprs)
        rows = [[str(eval(expr, {'r': resource} )) for expr in col_exprs] for resource in resources]
        # rows = [[str(col.find(resource)[0].value) for col in col_paths] for resource in resources]

        return [column_titles] + rows


def str_to_table(data: list[list[str]]) -> list[str]:
    col_lengths = [max(len(row[i]) for row in data) for i in range(len(data[0]))]
    for i, row in enumerate(data):
        data[i] = [f"{cell:<{col_lengths[j]}}" for j, cell in enumerate(row)]
        data[i] = "   ".join(data[i])
    return data
    
# valid_completion_items = [
#     ("Camila", "The reader of books."),
#     ("Carlos", "The writer of scripts."),
#     ("Sebastian", "The type hints guy."),
# ]

# usado para el autocompletado de recursos
# def complete_name(incomplete: str):
#     completion = []
#     for name, help_text in valid_completion_items:
#         if name.startswith(incomplete):
#             completion_item = (name, help_text)
#             completion.append(completion_item)
#     return completion


app = typer.Typer()
@app.command()
# def main(
#     name: Annotated[
#         str, typer.Option(help="The name to say hi to.", autocompletion=complete_name)
#     ] = "World",
# ):
def main( command):
    client = kr8s.api(kubeconfig=os.environ.get('KUBECONFIG'))
    config = load_config("./src/kkgepo/config.yaml")
    print(config)
    command = dealias(command, config)
    data = run_command(client, config, **command)
    table = str_to_table(data)
    selected = iterfzf(table, sort=False,__extra__= ['--height=13','--border', '--reverse', '--prompt=$ ', '--pointer=>', '--header-lines=1', '--color', 'header:reverse'])
    print(selected)


if __name__ == "__main__":
    app()