class ConnectingSameNodeError(Exception):
    """같은 노드끼리 간선으로 연결할 때 발생하는 에러"""


class AlreadyConnectedNodesError(Exception):
    """이미 연결된 노드끼리 간선으로 연결할 때 발생하는 에러"""
