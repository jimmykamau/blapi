from marshmallow import Schema, fields, ValidationError


def not_blank(data):
    if not data:
        raise ValidationError('Data not provided')


class BucketlistItemsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Bool(required=True)
    bucketlist_id = fields.Int()


class BucketlistSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    created_by = fields.Int()
    items = fields.Nested(
        BucketlistItemsSchema, key='id', many=True, dump_only=True)
