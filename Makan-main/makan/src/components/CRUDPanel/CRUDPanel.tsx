import React, { useState } from "react";
import CreateForm from "./CreateForm";

interface CRUDOperationsProps {
  modelName: string;
}

const CRUDOperations: React.FC<CRUDOperationsProps> = ({ modelName }) => {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [isCreateSectionOpen, setCreateSectionOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<any | null>(null); 

  const toSnakeCase = (str: string) => {
    if (str.endsWith("y")) {
      str = str.slice(0, -1) + "ie"; 
    }
    return str
      .replace(/([a-z])([A-Z])/g, "$1_$2")
      .toLowerCase();
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const endpoint = toSnakeCase(modelName) + "s";
      const response = await fetch(`${import.meta.env.VITE_API_URL}/${endpoint}`,{
        method: "GET",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      const result = await response.json();
      setData(result.data || []);
    } catch (error) {
      console.error(`Error fetching ${modelName} data:`, error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    setCreateSectionOpen(!isCreateSectionOpen);
    setEditingItem(null); 
  };

  const handleFormSubmit = async (formData: Record<string, any>) => {
    const token = localStorage.getItem("token");
    if (formData.images && typeof formData.images === "string") {
      formData.images = [formData.images];
    }

    try {
      const endpoint = toSnakeCase(modelName) + "s";
      const method = editingItem ? "PUT" : "POST"; 
      const url = editingItem
        ? `${import.meta.env.VITE_API_URL}/${endpoint}/${editingItem.id}`
        : `${import.meta.env.VITE_API_URL}/${endpoint}`;
      const response = await fetch(url, {
        method,
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        setCreateSectionOpen(false); 
        fetchData()
      } else {
        console.error(`Failed to ${editingItem ? "update" : "create"} ${modelName}`);
      }
    } catch (error) {
      console.error(`Error during ${editingItem ? "update" : "create"} operation:`, error);
    }
  };

  const handleEdit = (item: any) => {
    setEditingItem(item);
    setCreateSectionOpen(true); 
  };

  const handleDelete = async (id: number) => {
    const token = localStorage.getItem("token");
    const endpoint = toSnakeCase(modelName) + "s";

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/${endpoint}/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setData((prevData) => prevData.filter((item) => item.id !== id));
        console.log(`${modelName} with ID ${id} deleted successfully`);
      } else {
        console.error(`Failed to delete ${modelName} with ID ${id}`);
      }
    } catch (error) {
      console.error(`Error deleting ${modelName} with ID ${id}:`, error);
    }
  };

  return (
    <div>
      <div className="admin-buttons-sec">
        <button className="fetch-button" onClick={fetchData} disabled={loading}>
          {loading ? "Fetching..." : `Fetch ${modelName} Data`}
        </button>
        <button className="create-button" onClick={handleCreate}>
          +
        </button>
      </div>

      {isCreateSectionOpen && (
  <CreateForm
    modelName={modelName}
    onSubmit={handleFormSubmit}
    editingItem={editingItem} 
  />
)}


      {data.length > 0 ? (
        <table className="crud-table">
          <thead>
            <tr>
              {Object.keys(data[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                {Object.values(item).map((value, idx) => (
                  <td key={idx}>{String(value)}</td>
                ))}
                <td className="edit-delete-buttons">
                  <button
                    className="edit-button"
                    onClick={() => handleEdit(item)}
                  >
                    Edit
                  </button>
                  <button
                    className="delete-button"
                    onClick={() => handleDelete(item.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No data available for {modelName}.</p>
      )}
    </div>
  );
};

export default CRUDOperations;
