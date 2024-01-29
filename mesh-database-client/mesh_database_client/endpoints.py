import os

MESH_API_ENDPOINT_BASE = os.environ["MESH_API_ENDPOINT_BASE"]


MEMBER_LOOKUP_ENDPOINT = os.path.join(MESH_API_ENDPOINT_BASE, "member/lookup/")
INSTALL_LOOKUP_ENDPOINT = os.path.join(MESH_API_ENDPOINT_BASE, "install/lookup/")
BUILDINGS_ENDPOINT = os.path.join(MESH_API_ENDPOINT_BASE, "buildings/")
