// import React, { useEffect, useState } from "react";
// import axios from "axios";
// import { Link, useNavigate } from "react-router-dom";

// const baseUrl = "http://127.0.0.1:5000";

// function Home() {
//   const [users, setUsers] = useState([]);
//   const navigate = useNavigate();

//   useEffect(() => {
//     fetchUsers();
//   }, []);

//   const fetchUsers = async () => {
//     try {
//       const response = await axios.get(`${baseUrl}/users`);
//       setUsers(response.data.users);
//     } catch (error) {
//       console.error("Error fetching users:", error);
//     }
//   };

//   const handleEdit = (userId) => {
//     navigate(`/update-user/${userId}`);
//   };

//   const handleDelete = (userId) => {
//     // Implement logic for deleting user
//     console.log(`Delete user with ID ${userId}`);
//   };

//   const handleUserCreated = () => {
//     fetchUsers();
//   };

//   return (
//     <div className="bg-[#e8e6ed] p-8">
//       <div className="flex justify-between items-center mb-4">
//         <h1 className="text-2xl font-bold">User List</h1>
//         <Link to="/create-user">
//           <button
//             className="bg-[#5a56d6] text-white px-4 py-2 rounded"
//             onClick={() => {}}
//           >
//             Create User
//           </button>
//         </Link>
//       </div>
//       <table className="min-w-full border border-collapse border-gray-800">
//         <thead className="bg-gray-800 text-white">
//           <tr>
//             <th className="py-2 px-4 border-b">ID</th>
//             <th className="py-2 px-4 border-b">User Name</th>
//             <th className="py-2 px-4 border-b">Email</th>{" "}
//             <th className="py-2 px-4 border-b">Password</th>
//             <th className="py-2 px-4 border-b">Action</th>
//           </tr>
//         </thead>
//         <tbody>
//           {users.map((user) => (
//             <tr key={user.id} className="text-gray-800">
//               <td className="py-2 px-4 border-b">{user.id}</td>
//               <td className="py-2 px-4 border-b">{user.user_name}</td>
//               <td className="py-2 px-4 border-b">{user.email}</td>
//               <td className="py-2 px-4 border-b">{user.password}</td>
//               <td className="py-2 px-4 border-b">
//                 <button
//                   className="bg-blue-500 text-white px-2 py-1 mr-2 rounded"
//                   onClick={() => handleEdit(user.id)}
//                 >
//                   Edit
//                 </button>
//                 <Link to="/create-user">
//                   <button
//                     className="bg-red-500 text-white px-2 py-1 rounded"
//                     onClick={() => handleDelete(user.id)}
//                   >
//                     Delete
//                   </button>
//                 </Link>
//               </td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }

// export default Home;

// Home.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import DeleteDialog from "./DeleteDialog";

const baseUrl = "http://127.0.0.1:5000";

function Home() {
  const [users, setUsers] = useState([]);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [selectedUserId, setSelectedUserId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${baseUrl}/users`);
      setUsers(response.data.users);
    } catch (error) {
      console.error("Error fetching users:", error);
    }
  };

  const handleEdit = (userId) => {
    navigate(`/update-user/${userId}`);
  };

  const handleDelete = (userId) => {
    setSelectedUserId(userId);
    setShowDeleteDialog(true);
  };

  const handleDeleteConfirmation = async () => {
    try {
      await axios.delete(`${baseUrl}/users/${selectedUserId}`);
      setShowDeleteDialog(false);
      fetchUsers();
    } catch (error) {
      console.error("Error deleting user:", error);
    }
  };

  const handleDeleteCancel = () => {
    setShowDeleteDialog(false);
    setSelectedUserId(null);
  };

  const handleUserCreated = () => {
    fetchUsers();
  };

  return (
    <div className="bg-[#e8e6ed] p-8">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">User List</h1>
        <Link to="/create-user">
          <button
            className="bg-[#5a56d6] text-white px-4 py-2 rounded"
            onClick={() => {}}
          >
            Create User
          </button>
        </Link>
      </div>
      <table className="min-w-full border border-collapse border-gray-800">
        <thead className="bg-gray-800 text-white">
          <tr>
            <th className="py-2 px-4 border-b">ID</th>
            <th className="py-2 px-4 border-b">User Name</th>
            <th className="py-2 px-4 border-b">Email</th>{" "}
            <th className="py-2 px-4 border-b">Password</th>
            <th className="py-2 px-4 border-b">Action</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id} className="text-gray-800">
              <td className="py-2 px-4 border-b">{user.id}</td>
              <td className="py-2 px-4 border-b">{user.user_name}</td>
              <td className="py-2 px-4 border-b">{user.email}</td>
              <td className="py-2 px-4 border-b">{user.password}</td>
              <td className="py-2 px-4 border-b">
                <button
                  className="bg-blue-500 text-white px-2 py-1 mr-2 rounded"
                  onClick={() => handleEdit(user.id)}
                >
                  Edit
                </button>
                <button
                  className="bg-red-500 text-white px-2 py-1 rounded"
                  onClick={() => handleDelete(user.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {showDeleteDialog && (
        <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center bg-gray-800 bg-opacity-75">
          <DeleteDialog
            onDelete={handleDeleteConfirmation}
            onCancel={handleDeleteCancel}
          />
        </div>
      )}
    </div>
  );
}

export default Home;
