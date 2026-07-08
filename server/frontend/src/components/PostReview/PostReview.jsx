import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { addReview, fetchCarModels } from "../../api.js";

export default function PostReview() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [carModels, setCarModels] = useState([]);
  const [form, setForm] = useState({
    name: "",
    review: "",
    car_make: "",
    car_model: "",
    car_year: new Date().getFullYear(),
  });
  const [status, setStatus] = useState(null);

  useEffect(() => {
    fetchCarModels().then((data) => setCarModels(data.CarModels || []));
  }, []);

  const handleChange = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = await addReview({ ...form, dealership: Number(id) });
    if (result.status === 200) {
      setStatus("success");
      setTimeout(() => navigate(`/dealer/${id}`), 1200);
    } else {
      setStatus("error");
    }
  };

  return (
    <div>
      <h1>Post a Review</h1>
      <form className="review-form" onSubmit={handleSubmit}>
        <label>
          Your Name
          <input name="name" value={form.name} onChange={handleChange} required />
        </label>
        <label>
          Review
          <textarea name="review" rows={4} value={form.review} onChange={handleChange} required />
        </label>
        <label>
          Car Make / Model
          <select
            name="car_model"
            value={form.car_model}
            onChange={(event) => {
              const selected = carModels.find((cm) => cm.CarModel === event.target.value);
              setForm({
                ...form,
                car_model: event.target.value,
                car_make: selected ? selected.CarMake : "",
              });
            }}
            required
          >
            <option value="" disabled>Select a car model</option>
            {carModels.map((cm) => (
              <option key={`${cm.CarMake}-${cm.CarModel}`} value={cm.CarModel}>
                {cm.CarMake} {cm.CarModel}
              </option>
            ))}
          </select>
        </label>
        <label>
          Car Year
          <input type="number" name="car_year" min="1990" max="2030" value={form.car_year} onChange={handleChange} required />
        </label>
        <button type="submit" className="btn-primary">Post Review</button>
        {status === "success" && <p className="success-text">Review submitted!</p>}
        {status === "error" && <p className="error-text">Could not submit review. Please try again.</p>}
      </form>
    </div>
  );
}
