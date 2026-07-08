const mongoose = require("mongoose");

const dealerSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  full_name: { type: String, required: true },
  city: String,
  address: String,
  zip: String,
  state: String,
});

const reviewSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  name: { type: String, required: true },
  dealership: { type: Number, required: true },
  review: { type: String, required: true },
  purchase: { type: Boolean, default: false },
  purchase_date: String,
  car_make: String,
  car_model: String,
  car_year: Number,
});

module.exports = {
  Dealer: mongoose.model("Dealer", dealerSchema),
  Review: mongoose.model("Review", reviewSchema),
};
