const { gql } = require("apollo-server");

const typeDef = gql`
  type Character {
    name: String
    server: String
  }

  extend type Query {
    characters: [Character]
  }
`;

module.exports = {
  typeDef
};
