from urllib import request
from datetime import datetime
import simplejson
from pprint import pprint
import json

from graphqlclient import GraphqlClient

APPSYNC_ENDPOINT_DEV = ""
API_KEY = ""
POST_ID = "4d5b2637-598d-4f14-a9dd-95e3bdb901bf"

gp_client = None

delete_transport_mutation = """
mutation DeletePostAndComments($postId: ID!) {
  deletePostAndComments(postId: $postId) {
    id
  }
}
"""


def remove_post_and_comments():
    delete_variables = {
        "postId": POST_ID
    }

    result = gq_client.execute(
        query=delete_transport_mutation,
        operation_name='DeletePostAndComments',
        variables=delete_variables
    )
    print("DELETE RESULT:")
    print(result)


if __name__ == "__main__":
    gq_client = GraphqlClient(
        endpoint=APPSYNC_ENDPOINT_DEV,
        headers={'x-api-key': API_KEY}
    )
    remove_post_and_comments()
