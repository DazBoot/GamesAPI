const { ApolloServer, gql } = require("apollo-server");
const books = require("./books");
const characters = require("./characters");
const players = require("./players");

const typeDef = gql`
  type Query
`;

const server = new ApolloServer({
  typeDefs: [typeDef, books.typeDef, characters.typeDef, players.typeDef],
  resolvers: [books.resolvers, characters.resolvers, players.resolvers],
});

server.listen().then(({ url }) => {
  console.log(`🚀  Server ready at ${url}`);
});
