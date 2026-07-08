require("dotenv").config();
const fs = require("fs");
const path = require("path");
const mongoose = require("mongoose");

const { Dealer, Review } = require("./models");

const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/dealershipsDB";

async function seed() {
  await mongoose.connect(MONGO_URI);

  const dealerships = JSON.parse(fs.readFileSync(path.join(__dirname, "data", "dealerships.json")));
  const reviews = JSON.parse(fs.readFileSync(path.join(__dirname, "data", "reviews.json")));

  await Dealer.deleteMany({});
  await Review.deleteMany({});
  await Dealer.insertMany(dealerships);
  await Review.insertMany(reviews);

  console.log(`Seeded ${dealerships.length} dealers and ${reviews.length} reviews into ${MONGO_URI}`);
  await mongoose.disconnect();
}

if (require.main === module) {
  seed().catch((err) => {
    console.error("Seeding failed:", err);
    process.exit(1);
  });
}

module.exports = seed;
