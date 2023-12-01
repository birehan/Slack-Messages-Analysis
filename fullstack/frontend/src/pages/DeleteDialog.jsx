// DeleteDialog.js
import React from "react";

const DeleteDialog = ({ onDelete, onCancel }) => {
  return (
    <div className="bg-white p-4 border rounded shadow-md">
      <p>Are you sure you want to delete this user?</p>
      <div className="mt-4 flex justify-end">
        <button
          className="bg-red-500 text-white px-4 py-2 rounded mr-2"
          onClick={onDelete}
        >
          Delete
        </button>
        <button
          className="bg-gray-300 text-gray-800 px-4 py-2 rounded"
          onClick={onCancel}
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

export default DeleteDialog;
