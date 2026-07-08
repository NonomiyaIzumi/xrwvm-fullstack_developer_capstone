/**
 * Local-only dev entrypoint: boots a real (ephemeral, in-process) MongoDB via
 * mongodb-memory-server, seeds it with the demo dealers/reviews, then starts
 * the Express app against it. Not used in production/deployment, where
 * MONGO_URI should point at a real MongoDB instance (e.g. MongoDB Atlas).
 */
const { MongoMemoryServer } = require("mongodb-memory-server");

async function main() {
  const mongod = await MongoMemoryServer.create({ instance: { port: 27117 } });
  process.env.MONGO_URI = mongod.getUri("dealershipsDB");
  console.log(`In-memory MongoDB started at ${process.env.MONGO_URI}`);

  const seed = require("./populate_mongodb");
  await seed();

  const app = require("./app");
  const PORT = process.env.PORT || 3030;
  app.listen(PORT, () => console.log(`Dealership database service listening on port ${PORT}`));

  process.on("SIGINT", async () => {
    await mongod.stop();
    process.exit(0);
  });
}

main().catch((err) => {
  console.error("Failed to start local dealership database service:", err);
  process.exit(1);
});
