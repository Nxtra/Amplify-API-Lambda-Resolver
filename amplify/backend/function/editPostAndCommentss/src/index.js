const AWS = require("aws-sdk");

const docClient = new AWS.DynamoDB.DocumentClient();

const POSTTABLE = process.env.POSTTABLE;
const COMMENTTABLE = process.env.COMMENTTABLE;

const resolvers = {
  Mutation: {
    deletePostAndComments: (event) => {
      return deletePostAndComments(event);
    },
  },
};

exports.handler = async function (event, context) {
  console.log(event);
  console.log(context);

  const typeHandler = resolvers[event.typeName];
  if (typeHandler) {
    const resolver = typeHandler[event.fieldName];
    if (resolver) {
      return await resolver(event);
    }
  }
  throw new Error("Resolver not found.");
};

async function deletePostAndComments(event) {
  const removeCommentsProm = removeCommentsOfPost(event.arguments.postId);
  const removePostProm = removePost(event.arguments.postId);
  const [_, deletedPost] = await Promise.all([
    removeCommentsProm,
    removePostProm,
  ]);
  return { id: deletedPost.id };
}

async function removePost(postId) {
  const deletedPost = await deletePost(postId);
  return deletedPost;
}

async function removeCommentsOfPost(postId) {
  const comments = await listCommentsForPost(postId);
  await deleteComments(comments);
}

async function listCommentsForPost(postId) {
  var params = {
    TableName: COMMENTTABLE,
    IndexName: "byPost",
    KeyConditionExpression: "postID = :postId",
    ExpressionAttributeValues: { ":postId": postId },
  };
  try {
    const data = await docClient.query(params).promise();
    return data.Items;
  } catch (err) {
    return err;
  }
}

async function deleteComments(comments) {
  // format data for docClient
  const seedData = comments.map((item) => {
    return { DeleteRequest: { Key: { id: item.id } } };
  });

  /* We can only batch-write 25 items at a time,
    so we'll store both the quotient, as well as what's left.
    */

  let quotient = Math.floor(seedData.length / 25);
  const remainder = seedData.length % 25;
  /* Delete in increments of 25 */

  let batchMultiplier = 1;
  while (quotient > 0) {
    for (let i = 0; i < seedData.length - 1; i += 25) {
      docClient.batchWrite(
        {
          RequestItems: {
            [COMMENTTABLE]: seedData.slice(i, 25 * batchMultiplier),
          },
        },
        (err, data) => {
          if (err) {
            console.log(err);
            console.log("something went wrong...");
          } else {
            console.log("yay...deleted!");
          }
        }
      );
      console.log({ quotient });
      ++batchMultiplier;
      --quotient;
    }
  }

  /* Upload the remaining items (less than 25) */
  docClient.batchWrite(
    {
      RequestItems: {
        [COMMENTTABLE]: seedData.slice(seedData.length - remainder),
      },
    },
    (err, data) => {
      if (err) {
        console.log(err);
        console.log("something went wrong...");
      } else {
        console.log("yay...the remaining comments were deleted!");
      }
    }
  );
}

async function deletePost(id) {
  var params = {
    TableName: POSTTABLE,
    Key: { id },
    ReturnValues: "ALL_OLD",
  };
  try {
    const data = await docClient.delete(params).promise();
    const response = data.Attributes;
    return response;
  } catch (err) {
    return err;
  }
}
