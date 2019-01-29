from twisted.internet import defer

from aduser import db
from aduser.db import const as db_const, utils as db_utils
from tests import db_test_case


class DbInitTestCase(db_test_case):

    def test_get_mongo_db(self):
        database = db.get_mongo_db()
        self.assertIsNotNone(database)
        self.assertEqual(database.name, db_const.MONGO_DB_NAME)

    def test_get_mongo_connection(self):
        connection = db.get_mongo_connection()

        self.assertIs(connection, db.MONGO_CONNECTION)

    def test_get_collection(self):
        for name in ['data', 'user', 'pixel']:
            coll = db.get_collection(name)
            self.assertIsNotNone(coll)

    @defer.inlineCallbacks
    def test_configure_db(self):
        yield db.configure_db()

    @defer.inlineCallbacks
    def test_disconnect(self):
        disconnected = yield db.disconnect()
        self.assertIsNone(disconnected)

        connection = yield db.get_mongo_connection()
        self.assertIsNotNone(connection)
        self.assertIsNotNone(db.MONGO_CONNECTION)

        disconnected = yield db.disconnect()
        self.assertIsNone(disconnected)

    @defer.inlineCallbacks
    def test_get_collection_iter(self):
        l1, l2 = yield db_utils.get_collection_iter('data')
        self.assertListEqual([], l1)