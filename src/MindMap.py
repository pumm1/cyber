class Node:
    def __init__(self, row):
        self.id = row['id']
        self.title = row['title']
        self.info = row['info']
        self.x = row['pos_x']
        self.y = row['pos_y']

    def asJson(self):
        json = {
            'id': self.id,
            'title': self.title,
            'info': self.info,
            'x': self.x,
            'y': self.y
        }

        return json

class NodeConnection:
    def __init__(self, row):
        self.node_from = row['node_from']
        self.node_to = row['node_to']

    def asJson(self):
        json = {
            'from': self.node_from,
            'to': self.node_to
        }

        return json


class MindMap:
    def __init__(self, nodes: list[Node], connections: list[NodeConnection]):
        self.nodes = nodes
        self.connections = connections

    def asJson(self):
        nodes_json = list(map(lambda n: n.asJson(), self.nodes))
        connections_json = list(map(lambda c: c.asJson(), self.connections))

        json = {
            'nodes': nodes_json,
            'connections': connections_json
        }
        return json
