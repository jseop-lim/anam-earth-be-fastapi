class ConnectingSameNodeError(Exception):
    """같은 노드끼리 간선으로 연결할 때 발생하는 에러"""


class AlreadyConnectedNodesError(Exception):
    """이미 연결된 노드끼리 간선으로 연결할 때 발생하는 에러"""


class NoEdgeExistsBetweenNodesError(Exception):
    """주어진 노드 사이에 간선이 존재하지 않을 때 발생하는 에러"""
