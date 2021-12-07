from dataclasses import dataclass


@dataclass
class GraphqlAttr:
    type_name: str
    array: bool = False
    required: bool = True

    def to_graphql(self):
        graphql = self.type_name
        if self.array:
            graphql = f'[{graphql}]'
        if self.required:
            graphql = graphql + '!'
        return graphql
