# TODO: Convert this to helm config file

TARKOV_ENDPOINT = 'https://api.tarkov.dev/graphql'

# Turn this into a database at some point?
CACHE_DIR = "datastore"
THIS_DIR = f"adapters/datastore/"
PATHS = {
    "tasks": f"{THIS_DIR}tasks.json"
}