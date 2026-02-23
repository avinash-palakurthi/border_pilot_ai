import { useState } from "react";
const API_BASE = import.meta.env.VITE_API_URL;
export default function UploadForm({ onSuccess }) {
  const [cmr, setCmr] = useState(null);
  const [invoice, setInvoice] = useState(null);
  const [packingList, setPackingList] = useState(null);
  const [adrCert, setAdrCert] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!cmr || !invoice) {
      alert("CMR and Invoice are required documents.");
      return;
    }

    const formData = new FormData();
    formData.append("cmr", cmr);
    formData.append("invoice", invoice);

    if (packingList) formData.append("packing_list", packingList);
    if (adrCert) formData.append("adr_certificate", adrCert);

    try {
      setLoading(true);

      const response = await fetch(`${API_BASE}/extract`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.status === "pending_review") {
        onSuccess(data.data);
      } else {
        alert("Unexpected response from server");
      }
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const FileInput = ({ label, required, file, setter }) => {
    return (
      <div className="space-y-2">
        <label className="block text-white font-medium">
          {label} {required && <span className="text-red-400">*</span>}
        </label>

        {/* Hidden real input */}
        <input
          type="file"
          accept="image/*,.pdf"
          capture="environment"
          id={label}
          onChange={(e) => setter(e.target.files[0])}
          className="hidden"
        />

        {/* Custom button */}
        <label
          htmlFor={label}
          className="cursor-pointer inline-block bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold"
        >
          {file ? "Change File" : "Choose File"}
        </label>

        {/* Show selected file */}
        {file && (
          <p className="text-sm text-green-400">Selected: {file.name}</p>
        )}
      </div>
    );
  };

  return (
    <div className="bg-gray-800 p-8 rounded-xl shadow-lg max-w-xl mx-auto space-y-8">
      <form onSubmit={handleSubmit} className="space-y-8">
        {/* Required Section */}
        <div>
          <h3 className="text-lg font-semibold text-white mb-4 border-b border-gray-600 pb-2">
            Required Documents
          </h3>

          <FileInput
            label="CMR Document"
            required={true}
            file={cmr}
            setter={setCmr}
          />
          <FileInput
            label="Commercial Invoice"
            required={true}
            file={invoice}
            setter={setInvoice}
          />
        </div>

        {/* Optional Section */}
        {/* <div>
          <h3 className="text-lg font-semibold text-gray-300 mb-4 border-b border-gray-700 pb-2">
            Optional Documents
          </h3>

          <FileInput
            label="Packing List"
            required={false}
            file={packingList}
            setter={setPackingList}
          />
          <FileInput
            label="ADR Certificate (Dangerous Goods)"
            required={false}
            file={adrCert}
            setter={setAdrCert}
          />
        </div> */}

        {/* Submit */}
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition"
        >
          {loading ? "Extracting Documents..." : "Upload & Extract"}
        </button>
      </form>
    </div>
  );
}
