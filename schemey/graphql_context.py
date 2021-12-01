from dataclasses import field, dataclass
from io import StringIO
from typing import Dict, TextIO, Optional

from schemey.graphql.graphql_object_type import GraphqlObjectType


@dataclass
class GraphqlContext:
    object_type: GraphqlObjectType
    # noinspection PyUnresolvedReferences
    objects: Dict[str, 'schemey.graphql.ObjectSchema'] = field(default_factory=dict)
    # noinspection PyUnresolvedReferences
    enums: Dict[str, 'schemey.graphql.EnumSchema'] = field(default_factory=dict)
    # noinspection PyUnresolvedReferences
    unions: Dict[str, 'schemey.graphql.AnyOfSchema'] = field(default_factory=dict)

    def to_graphql(self, writer: Optional[TextIO] = None):
        local_writer = writer or StringIO()
        for e in self.enums.values():
            e.to_graphql(local_writer)
        for obj in self.objects.values():
            obj.to_graphql(local_writer, self.object_type)
        for u in self.unions.values():
            u.to_graphql(local_writer)
        if writer is None:
            return local_writer.getvalue()
