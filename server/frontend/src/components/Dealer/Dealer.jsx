import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchDealer, fetchDealerReviews } from "../../api.js";

export default function Dealer({ user }) {
  const { id } = useParams();
  const [dealer, setDealer] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [reviewsLoaded, setReviewsLoaded] = useState(false);

  useEffect(() => {
    setReviewsLoaded(false);
    fetchDealer(id).then((data) => setDealer(data.dealer));
    fetchDealerReviews(id).then((data) => {
      setReviews(Array.isArray(data.reviews) ? data.reviews : []);
      setReviewsLoaded(true);
    });
  }, [id]);

  if (!dealer) return <p>Loading dealer...</p>;

  return (
    <div>
      <h1>{dealer.full_name}</h1>
      <p>
        {dealer.address}, {dealer.city}, {dealer.state} {dealer.zip}
      </p>

      {user && user.isAuthenticated && (
        <p>
          <Link to={`/postreview/${id}`} className="btn-primary" style={{ textDecoration: "none", padding: "0.5rem 1rem" }}>
            Review Dealer
          </Link>
        </p>
      )}

      <h2>Reviews</h2>
      {!reviewsLoaded && <p>Loading reviews...</p>}
      {reviewsLoaded && reviews.length === 0 && <p>No reviews yet for this dealer.</p>}
      {reviews.map((review, index) => (
        <div className="review-card" key={review._id || index}>
          <p>{review.review}</p>
          <p>
            <strong>{review.name}</strong> &mdash; {review.car_make} {review.car_model} ({review.car_year})
          </p>
          <p className={`sentiment-${review.sentiment || "neutral"}`}>
            Sentiment: {review.sentiment || "neutral"}
          </p>
        </div>
      ))}
    </div>
  );
}
