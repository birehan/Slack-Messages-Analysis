// UpdateUser.js

import React, { useState, useEffect } from "react";
import axios from "axios";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useNavigate, useParams } from "react-router-dom";

const UpdateUser = () => {
  const navigate = useNavigate();
  const { userId } = useParams();

  const [user, setUser] = useState({
    user_name: "",
    email: "",
    password: "",
  });

  useEffect(() => {
    fetchUser();
  }, [userId]);

  const fetchUser = async () => {
    try {
      const response = await axios.get(`http://127.0.0.1:5000/users/${userId}`);
      setUser(response.data.user);
    } catch (error) {
      console.error("Error fetching user:", error);
    }
  };

  const handleChange = (e) => {
    setUser({
      ...user,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put(
        `http://127.0.0.1:5000/users/${userId}`,
        user
      );
      toast.success("User updated successfully");
      console.log("User updated successfully:", response.data);
      navigate("/");
    } catch (error) {
      toast.error("Error updating user");
      console.error("Error updating user:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto bg-white p-8 border rounded shadow-md mt-8">
      <h2 className="text-2xl font-semibold mb-4">Update User</h2>
      <form onSubmit={handleSubmit}>
        {/* ... (similar input fields as CreateUser for updating) ... */}
        <div className="mb-4">
          <label
            htmlFor="user_name"
            className="block text-sm text-left font-medium text-gray-600"
          >
            User Name:
          </label>
          <input
            type="text"
            id="user_name"
            name="user_name"
            value={user.user_name}
            onChange={handleChange}
            className="mt-1 p-2 border rounded-md w-full focus:outline-none focus:ring focus:border-blue-300"
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="email"
            className="block text-sm text-left font-medium text-gray-600"
          >
            Email:
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={user.email}
            onChange={handleChange}
            className="mt-1 p-2 border rounded-md w-full focus:outline-none focus:ring focus:border-blue-300"
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="password"
            className="block text-sm text-left font-medium text-gray-600"
          >
            Password:
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={user.password}
            onChange={handleChange}
            className="mt-1 p-2 border rounded-md w-full focus:outline-none focus:ring focus:border-blue-300"
          />
        </div>

        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 focus:outline-none focus:ring focus:border-blue-300"
        >
          Update User
        </button>
      </form>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </div>
  );
};

export default UpdateUser;
