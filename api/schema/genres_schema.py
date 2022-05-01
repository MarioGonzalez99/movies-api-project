from api.schema.schema import ma


class GenresSchema(ma.Schema):
    class Meta:
        fields = ('genre_id', 'name')
