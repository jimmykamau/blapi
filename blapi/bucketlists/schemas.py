from marshmallow import Schema, fields, ValidationError


def not_blank(data):
    if not data:
        raise ValidationError('Data not provided')


class BucketlistSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    created_by = fields.Int()


class BucketlistItemsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Bool()
    bucketlist_id = fields.Int()