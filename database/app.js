require("dotenv").config();
const cors = require("cors");
const express = require("express");
const mongoose = require("mongoose");

const { Dealer, Review } = require("./models");

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3030;
const MONGO_URI = process.env.MONGO_URI || "mongodb://localhost:27017/dealershipsDB";

mongoose
  .connect(MONGO_URI)
  .then(() => console.log(`Connected to MongoDB at ${MONGO_URI}`))
  .catch((err) => console.error("MongoDB connection error:", err));

app.get("/", (req, res) => {
  res.send("Dealership database microservice is running.");
});

app.get("/fetchDealers", async (req, res) => {
  const dealers = await Dealer.find();
  res.json(dealers);
});

app.get("/fetchDealers/:state", async (req, res) => {
  const dealers = await Dealer.find({ state: req.params.state });
  res.json(dealers);
});

app.get("/fetchDealer/:id", async (req, res) => {
  const dealer = await Dealer.findOne({ id: Number(req.params.id) });
  res.json(dealer);
});

app.get("/fetchReviews", async (req, res) => {
  const reviews = await Review.find();
  res.json(reviews);
});

app.get("/fetchReviews/dealer/:id", async (req, res) => {
  const reviews = await Review.find({ dealership: Number(req.params.id) });
  res.json(reviews);
});

app.post("/insert_review", async (req, res) => {
  try {
    const last = await Review.findOne().sort({ id: -1 });
    const nextId = last ? last.id + 1 : 1;
    const review = new Review({ ...req.body, id: nextId });
    await review.save();
    res.status(201).json(review);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

if (require.main === module) {
  app.listen(PORT, () => console.log(`Dealership database service listening on port ${PORT}`));
}

module.exports = app;
