import React, { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { fetchDealers } from "../../api.js";

const STATES = ["All", "California", "Colorado", "Florida", "Kansas", "New York", "Texas"];

export default function Dealers({ user }) {
  const { state } = useParams();
  const navigate = useNavigate();
  const [dealers, setDealers] = useState([]);
  const [loading, setLoading] = useState(true);
  const selected = state || "All";

  useEffect(() => {
    setLoading(true);
    fetchDealers(selected).then((data) => {
      setDealers(data.dealers || []);
      setLoading(false);
    });
  }, [selected]);

  return (
    <div>
      <h1>Dealers</h1>
      <div className="state-filter">
        <label htmlFor="state-select">Filter by state: </label>
        <select
          id="state-select"
          value={selected}
          onChange={(event) => {
            const value = event.target.value;
            navigate(value === "All" ? "/dealers" : `/dealers/${value}`);
          }}
        >
          {STATES.map((option) => (
            <option key={option} value={option}>{option}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <p>Loading dealers...</p>
      ) : (
        <table className="dealer-table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Name</th>
              <th>City</th>
              <th>State</th>
              <th>Zip</th>
              {user && user.isAuthenticated && <th>Review</th>}
            </tr>
          </thead>
          <tbody>
            {dealers.map((dealer) => (
              <tr key={dealer.id}>
                <td>{dealer.id}</td>
                <td><Link to={`/dealer/${dealer.id}`}>{dealer.full_name}</Link></td>
                <td>{dealer.city}</td>
                <td>{dealer.state}</td>
                <td>{dealer.zip}</td>
                {user && user.isAuthenticated && (
                  <td><Link to={`/postreview/${dealer.id}`}>Review Dealer</Link></td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
