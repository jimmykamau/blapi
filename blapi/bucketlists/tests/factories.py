from datetime import datetime
import factory
from ..models import Bucketlist, BucketlistItems
from ...authorization.tests.factories import UserFactory


class BucketlistFactory(factory.Factory):
    class Meta:
        model = Bucketlist

    name = factory.Sequence(lambda n: "My bucketlist %d" % n)
    date_created = factory.LazyFunction(datetime.now)
    date_modified = factory.LazyFunction(datetime.now)
    created_by = factory.SubFactory(UserFactory)


class BucketlistItemsFactory(factory.Factory):
    class Meta:
        model = BucketlistItems

    name = factory.Sequence(lambda n: "My bucketlist %d item" % n)
    date_created = factory.LazyFunction(datetime.now)
    date_modified = factory.LazyFunction(datetime.now)
    done = False
    bucketlist_id = factory.SubFactory(BucketlistFactory)
