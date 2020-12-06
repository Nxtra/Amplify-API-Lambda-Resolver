from urllib import request
from datetime import datetime
import simplejson
from pprint import pprint
import json

from graphqlclient import GraphqlClient
from auth import get_access_token

APPSYNC_ENDPOINT_DEV = "https://ouchezcbknfi3moeec6zkkspnu.appsync-api.eu-west-1.amazonaws.com/graphql"

gp_client = None

list_transports_query = """
query listTransports {
  listTransports {
    items {
      attachment
      comment
      id
    }
  }
}

"""

get_transport_query = """
query getTransport($getInput: ID!) {
  getTransport(id: $getInput) {
      attachment
      comment
      containerNumber
      createdAt
      customer {
        name
      }
      description
      plannedDate
      genset
      id
      transportSupplierPrice
      transportCustomerPrice
      updatedAt
  }
}
"""

create_transport_mutation = """
  mutation createTransport {
  createTransport(input: {plannedDate: "2020-09-25", transportCustomerId: "cust-092", transportCustomerPrice: 740, transportSupplierPrice: 600, genset: false}) {
    id
  }
}
"""

delete_transport_mutation = """
mutation deleteTransport($deleteInput: DeleteTransportInput!) {
  deleteTransport(input: $deleteInput) {
    id
  }
}
"""


def execute_test_scenario():
    # CREATE A TRANSPORT
    result = gq_client.execute(
        query=create_transport_mutation,
        operation_name='createTransport'
    )
    print("CREATE RESULT:")
    print(result)
    newly_created_transport_id = result.get("data")["createTransport"]["id"]

    # LIST ALL TRANSPORTS
    result = gq_client.execute(
        query=list_transports_query,
        operation_name='listTransports'
    )
    print("LIST RESULT:")
    print(result)

    # GET ONE TRANSPORT
    get_variables = {
        "getInput": newly_created_transport_id
    }

    result = gq_client.execute(
        query=get_transport_query,
        operation_name='getTransport',
        variables=get_variables
    )
    print("GET RESULT:")
    print(result)

    # DELETE TRANSPORT
    delete_variables = {
        "deleteInput": {
            "id": newly_created_transport_id
        }
    }

    result = gq_client.execute(
        query=delete_transport_mutation,
        operation_name='deleteTransport',
        variables=delete_variables
    )
    print("DELETE RESULT:")
    print(result)


if __name__ == "__main__":
    access_token = get_access_token()
    gq_client = GraphqlClient(
        endpoint=APPSYNC_ENDPOINT_DEV,
        headers={'authorization': access_token}
    )
    execute_test_scenario()
