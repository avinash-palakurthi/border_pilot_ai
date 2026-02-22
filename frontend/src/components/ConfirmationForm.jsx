import { useState } from "react";

export default function ConfirmationForm({ extractedData, onValidated }) {
  const [formData, setFormData] = useState(extractedData || {});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleValidate = async () => {
    try {
      setLoading(true);

      // 🔥 Bulletproof cleaning
      const cleanedData = {
        ...formData,

        gross_weight:
          formData.gross_weight === "" ||
          formData.gross_weight === undefined ||
          formData.gross_weight === null
            ? null
            : Number(formData.gross_weight),

        un_number:
          formData.un_number === "" ||
          formData.un_number === undefined ||
          formData.un_number === null
            ? null
            : formData.un_number.trim(),

        shipper_vat:
          formData.shipper_vat === "" ||
          formData.shipper_vat === undefined ||
          formData.shipper_vat === null
            ? null
            : formData.shipper_vat.trim(),

        receiver_vat:
          formData.receiver_vat === "" ||
          formData.receiver_vat === undefined ||
          formData.receiver_vat === null
            ? null
            : formData.receiver_vat.trim(),
      };

      console.log("Sending to backend:", cleanedData); // 👈 Debug

      const response = await fetch("http://127.0.0.1:8000/validate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(cleanedData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Backend error:", errorData);
        alert("Validation failed: Check console");
        return;
      }

      const result = await response.json();
      onValidated(result);
    } catch (error) {
      console.error("Validation failed:", error);
      alert("Validation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 p-6 rounded-xl space-y-4">
      <h2 className="text-xl font-semibold mb-4">
        Review & Confirm Shipment Data
      </h2>

      {Object.keys(formData).map((key) => (
        <div key={key}>
          <label className="block text-sm text-gray-300 mb-1 capitalize">
            {key.replace(/_/g, " ")}
          </label>

          <input
            type="text"
            name={key}
            value={formData[key] ?? ""} /* 🔥 Important fix */
            onChange={handleChange}
            className="w-full p-2 rounded bg-gray-700 text-white border border-gray-600"
          />
        </div>
      ))}

      <button
        onClick={handleValidate}
        disabled={loading}
        className="w-full bg-green-600 hover:bg-green-700 text-white py-2 rounded-lg font-semibold"
      >
        {loading ? "Validating..." : "Confirm & Validate"}
      </button>
    </div>
  );
}
