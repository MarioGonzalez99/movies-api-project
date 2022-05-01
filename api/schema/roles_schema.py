from api.schema.schema import ma


class RolesSchema(ma.Schema):
    class Meta:
        fields = ('rol_id', 'name')
