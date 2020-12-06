from urllib import request
from datetime import datetime
import simplejson
from pprint import pprint
import json
from random import choice
from string import ascii_lowercase, digits

from graphqlclient import GraphqlClient

APPSYNC_ENDPOINT_DEV = ""
API_KEY = ""

gp_client = None


create_blog_mutation = """
mutation CreateBlog {
  createBlog(input: {name: "theclouddeveloper.io"}) {
    id
    name
  }
}
"""

create_post_mutation = """
mutation CreatePost($blogId: ID!){
  createPost(input: {blogID: $blogId, title: "Amplify custom lambda resolver"}) {
    id
  }
}
"""

create_comment_mutation = """
mutation CreateComment($postId: ID!, $commentText: String!) {
  createComment(input: {postID: $postId, content: $commentText}) {
    id
  }
}
"""


def execute_test_scenario():
    # CREATE A BLOG
    result = gq_client.execute(
        query=create_blog_mutation,
        operation_name='CreateBlog'
    )
    print("CREATE BLOG RESULT:")
    print(result)
    newly_created_blog_id = result.get("data")["createBlog"]["id"]

    # CREATE A POST
    create_post_variables = {
        "blogId": newly_created_blog_id
    }
    result = gq_client.execute(
        query=create_post_mutation,
        operation_name='CreatePost',
        variables=create_post_variables
    )
    print("CREATE post RESULT:")
    print(result)
    newly_created_post_id = result.get("data")["createPost"]["id"]

    create_comments(newly_created_post_id, 500)

    # CREATE A 1000 comments


def create_comments(postId, number_of_comments):
    comments = get_list_of_random_comments(number_of_comments)

    for i in range(number_of_comments):
        create_comment_variables = {
            "postId": postId,
            "commentText": comments[i]
        }
        gq_client.execute(
            query=create_comment_mutation,
            operation_name='CreateComment',
            variables=create_comment_variables
        )


def get_list_of_random_comments(length):
    chars = ascii_lowercase + digits
    lst = [''.join(choice(chars) for _ in range(12)) for _ in range(length)]
    return lst


if __name__ == "__main__":
    gq_client = GraphqlClient(
        endpoint=APPSYNC_ENDPOINT_DEV,
        headers={'x-api-key': API_KEY}
    )
    execute_test_scenario()
