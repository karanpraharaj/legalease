import os

import pymongo
from pymongo.collection import ReturnDocument

import uuid
import logging


new_progress_status = 'New'
processing_ready_status = 'Processing Ready'
processing_in_progress_status = 'Processing In Progress'
process_finished_status = 'Processing Finished'
process_error_status = 'Error'
process_finished_with_error_status = 'Processing Finished With Errors'
process_stop_requested_status = 'Processing Stop Requested'
process_stopped_status = 'Processing Stopped'

processing_string_to_status = {
    new_progress_status: 0,
    processing_ready_status: 1,
    processing_in_progress_status: 2,
    process_finished_status: 3,
    process_error_status: 4,
    process_stop_requested_status: 6,
    process_stopped_status: 5,
    process_finished_with_error_status: 9,
}

processing_status_to_string = {value: key for key, value in processing_string_to_status.items()}

database = 'legalease'


def get_mongo_connection_string():
    mongo_user = os.getenv('MONGO_USER')
    mongo_password = os.getenv('MONGO_PASSWORD')
    mongo_host = os.getenv('MONGO_HOST')
    mongo_port = os.getenv('MONGO_PORT')
    mongo_connection_string = f'mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin'
    return mongo_connection_string


def return_mongo_conn():
    try:
        logging.debug('Attempting to open mongo connection.')
        conn_string = get_mongo_connection_string()
        new_conn = pymongo.MongoClient(host=conn_string)
        return new_conn
    except Exception as error:
        raise ConnectionError('Cannot open Mongo DB with: {}'.format(error))


def mongo_find(collection, find_filter, fields=None, hint=None):
    mongo_connection, cursor = mongo_find_cursor(collection, find_filter, fields=fields, hint=hint)
    entries = [document for document in cursor]
    cursor.close()
    mongo_connection.close()
    return entries


def mongo_find_cursor(collection, find_filter, fields=None, hint=None):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    cursor = mongo_collection.find(find_filter, projection=fields, no_cursor_timeout=True)
    if hint is not None:
        cursor.hint([(hint, 1)])
    return mongo_connection, cursor


def mongo_insert_one(collection, document):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    inserted_id = mongo_collection.insert_one(document).inserted_id
    mongo_connection.close()
    return inserted_id


def mongo_find_one_id(collection, _id):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    result = mongo_collection.find_one({'_id': _id}, no_cursor_timeout=True)
    mongo_connection.close()
    return result


def mongo_find_one_and_upsert(collection, document):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    upserted_document = mongo_collection.find_one_and_update(
        {'_id': document['_id']},
        {'$set': document},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    mongo_connection.close()
    return upserted_document


def mongo_find_oldest_and_delete(collection):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    deleted_value = mongo_collection.find_one_and_delete({}, sort=[('_id', pymongo.ASCENDING)])
    mongo_connection.close()
    return deleted_value


def return_work_queue_name(work_type):
    work_queue_collection_name = '{}_queue'.format(work_type)
    return work_queue_collection_name


def return_work_batch_storage_name(work_type):
    work_batch_storage_collection_name = '{}_batch'.format(work_type)
    return work_batch_storage_collection_name


def get_new_work_token(work_type):
    work_queue_collection_name = return_work_queue_name(work_type)
    new_work_token = mongo_find_oldest_and_delete(work_queue_collection_name)
    return new_work_token


def upsert_work_token_to_batch_storage(work_type, token):
    work_queue_collection_name = return_work_batch_storage_name(work_type)
    upserted_token = mongo_find_one_and_upsert(work_queue_collection_name, token)
    return upserted_token


def mongo_set_id(collection, document_id, set_field, set_key, set_value):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    if set_field is not None:
        set_object = {'{}.{}'.format(set_field, set_key): set_value}
    else:
        set_object = {set_key: set_value}
    mongo_collection.update(
        {'_id': document_id},
        {'$set': set_object}
    )
    mongo_connection.close()


def mongo_unset_id(collection, document_id, unset_field, unset_key):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    if unset_field is not None:
        unset_object = {'{}.{}'.format(unset_field, unset_key): ""}
    else:
        unset_object = {unset_key: ""}
    mongo_collection.update(
        {'_id': document_id},
        {'$unset': unset_object}
    )
    mongo_connection.close()


def mongo_delete_many(collection, find_filter):
    mongo_connection = return_mongo_conn()
    mongo_collection = mongo_connection[database][collection]
    mongo_collection.delete_many(find_filter)
    mongo_connection.close()


def submit_new_batch_token(work_type, token):
    work_batch_storage_collection_name = return_work_batch_storage_name(work_type)
    mongo_insert_one(work_batch_storage_collection_name, token)


def set_progress(token, progress_descriptor):
    token['status'] = progress_descriptor
    token['reveal_status_int'] = processing_string_to_status.get(progress_descriptor, -1)


def set_and_commit_progress(collection, document_id, progress_descriptor):
    mongo_set_id(collection, document_id, None, 'status', progress_descriptor)
    mongo_set_id(collection, document_id, None, 'reveal_status_int', processing_string_to_status.get(progress_descriptor, -1))
