// import { useState } from "react";
// import UploadForm from "./components/UploadForm";
// import ConfirmationForm from "./components/ConfirmationForm";

// function App() {
//   const [step, setStep] = useState(1);
//   const [data, setData] = useState(null);
//   const [result, setResult] = useState(null);
//   const [notification, setNotification] = useState(null);
//   const [retryCount, setRetryCount] = useState(0);

//   const handleExtractSuccess = (extractedData) => {
//     setData(extractedData);
//     setStep(3);
//   };

//   const handleValidationResult = (validationResult) => {
//     setResult(validationResult);

//     // If RED → show modal (handled below)
//     if (validationResult.status === "red" && validationResult.notification) {
//       setNotification(validationResult.notification);
//     } else {
//       // If yellow or green → go directly to step 5
//       setRetryCount(0);
//       setStep(5);
//     }
//   };

//   const steps = [
//     "Upload",
//     "Extracting",
//     "Driver Confirmation",
//     "Evaluating",
//     "Final Output",
//   ];

//   return (
//     <div className="min-h-screen bg-gray-900 text-white p-8 relative">
//       <h1 className="text-3xl font-bold mb-8">BORDERPILOT AI</h1>

//       {/* Progress Bar */}
//       <div className="flex justify-between mb-10">
//         {steps.map((label, index) => {
//           const stepNumber = index + 1;
//           return (
//             <div key={label} className="flex flex-col items-center flex-1">
//               <div
//                 className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
//                   ${
//                     stepNumber < step
//                       ? "bg-green-500 text-black"
//                       : stepNumber === step
//                         ? "bg-blue-500"
//                         : "bg-gray-600"
//                   }`}
//               >
//                 {stepNumber}
//               </div>
//               <p className="text-xs mt-2 text-center">{label}</p>
//             </div>
//           );
//         })}
//       </div>

//       {/* Step 1 */}
//       {step === 1 && <UploadForm onSuccess={handleExtractSuccess} />}

//       {/* Step 3 */}
//       {step === 3 && data && (
//         <ConfirmationForm
//           extractedData={data}
//           onValidated={handleValidationResult}
//         />
//       )}

//       {/* Step 5 */}
//       {step === 5 && result && (
//         <div className="bg-gray-800 p-6 rounded-xl">
//           <h2 className="text-xl font-semibold mb-4">Validation Result</h2>

//           <p className="text-lg font-bold mb-2">
//             Status:{" "}
//             <span
//               className={`${
//                 result.status === "red"
//                   ? "text-red-500"
//                   : result.status === "yellow"
//                     ? "text-yellow-400"
//                     : "text-green-400"
//               }`}
//             >
//               {/* VIES Verification Section */}
//               {result.vies_verification && (
//                 <div className="mt-6 bg-gray-700 p-4 rounded-lg text-sm">
//                   <h3 className="text-md font-semibold mb-3 text-white">
//                     VAT Verification (VIES)
//                   </h3>

//                   {/* Receiver VAT */}
//                   {result.vies_verification.receiver && (
//                     <div className="mb-3">
//                       <p>
//                         <span className="font-semibold">Receiver VAT:</span>{" "}
//                         {data?.receiver_vat || "N/A"}
//                       </p>

//                       {result.vies_verification.receiver.error ? (
//                         <p className="text-yellow-400">
//                           VIES service unavailable – manual verification
//                           required.
//                         </p>
//                       ) : (
//                         <>
//                           <p>
//                             <span className="font-semibold">VIES Status:</span>{" "}
//                             {result.vies_verification.receiver.valid ? (
//                               <span className="text-green-400">VALID</span>
//                             ) : (
//                               <span className="text-red-400">INVALID</span>
//                             )}
//                           </p>

//                           {result.vies_verification.receiver
//                             .verification_token && (
//                             <p className="text-blue-400 break-all">
//                               Verification Token:{" "}
//                               {
//                                 result.vies_verification.receiver
//                                   .verification_token
//                               }
//                             </p>
//                           )}
//                         </>
//                       )}
//                     </div>
//                   )}

//                   {/* Shipper VAT */}
//                   {result.vies_verification.shipper && (
//                     <div>
//                       <p>
//                         <span className="font-semibold">Shipper VAT:</span>{" "}
//                         {data?.shipper_vat || "N/A"}
//                       </p>

//                       {result.vies_verification.shipper.error ? (
//                         <p className="text-yellow-400">
//                           VIES service unavailable – manual verification
//                           required.
//                         </p>
//                       ) : (
//                         <>
//                           <p>
//                             <span className="font-semibold">VIES Status:</span>{" "}
//                             {result.vies_verification.shipper.valid ? (
//                               <span className="text-green-400">VALID</span>
//                             ) : (
//                               <span className="text-red-400">INVALID</span>
//                             )}
//                           </p>

//                           {result.vies_verification.shipper
//                             .verification_token && (
//                             <p className="text-blue-400 break-all">
//                               Verification Token:{" "}
//                               {
//                                 result.vies_verification.shipper
//                                   .verification_token
//                               }
//                             </p>
//                           )}
//                         </>
//                       )}
//                     </div>
//                   )}
//                 </div>
//               )}
//             </span>
//           </p>

//           {/* Issues */}
//           {result.issues?.length > 0 && (
//             <ul className="list-disc pl-5 text-red-400">
//               {result.issues.map((issue, i) => (
//                 <li key={i}>{issue}</li>
//               ))}
//             </ul>
//           )}

//           {/* Warnings */}
//           {result.warnings?.length > 0 && (
//             <ul className="list-disc pl-5 text-yellow-400 mt-4">
//               {result.warnings.map((warn, i) => (
//                 <li key={i}>{warn}</li>
//               ))}
//             </ul>
//           )}

//           {/* Yellow Banner */}
//           {result.notification?.type === "warning" && (
//             <div className="mt-6 bg-yellow-600 text-black p-4 rounded-lg font-semibold">
//               ⚠ {result.notification.message}
//             </div>
//           )}

//           {/* AI Compliance Report */}
//           {result.ai_report && (
//             <div className="mt-6 bg-gray-700 p-5 rounded-lg">
//               <h3 className="text-lg font-semibold mb-3">
//                 AI Compliance Assessment
//               </h3>
//               <p className="text-gray-300 whitespace-pre-line">
//                 {result.ai_report}
//               </p>
//             </div>
//           )}
//         </div>
//       )}

//       {/* 🔴 Critical Modal (Blocking) */}
//       {notification && notification.type === "critical" && (
//         <div className="fixed inset-0 flex items-center justify-center bg-black/80 z-50">
//           <div className="bg-red-700 text-white p-8 rounded-xl max-w-md w-full shadow-lg">
//             <h3 className="text-xl font-bold mb-4">🚨 Shipment Blocked</h3>

//             <p className="mb-6">{notification.message}</p>

//             <button
//               onClick={() => {
//                 setNotification(null);

//                 if (retryCount >= 1) {
//                   // After second failure → show final output
//                   setStep(5);
//                 } else {
//                   // First failure → allow correction
//                   setRetryCount((prev) => prev + 1);
//                   setStep(3);
//                 }
//               }}
//               className="w-full bg-black hover:bg-gray-800 py-2 rounded-lg font-semibold"
//             >
//               Acknowledge & Recheck
//             </button>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;

import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ConfirmationForm from "./components/ConfirmationForm";

function App() {
  const [step, setStep] = useState(1);
  const [data, setData] = useState(null);
  const [confirmedData, setConfirmedData] = useState(null); // ✅ NEW: stores driver-confirmed data
  const [result, setResult] = useState(null);
  const [notification, setNotification] = useState(null);
  const [retryCount, setRetryCount] = useState(0);

  const handleExtractSuccess = (extractedData) => {
    setData(extractedData);
    setStep(3);
  };

  // ✅ FIXED: now receives submittedData from ConfirmationForm
  const handleValidationResult = (validationResult, submittedData) => {
    setConfirmedData(submittedData); // ✅ store corrected data
    setResult(validationResult);

    if (validationResult.status === "red" && validationResult.notification) {
      setNotification(validationResult.notification);
    } else {
      setRetryCount(0);
      setStep(5);
    }
  };

  const steps = [
    "Upload",
    "Extracting",
    "Driver Confirmation",
    "Evaluating",
    "Final Output",
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8 relative">
      <h1 className="text-3xl font-bold mb-8">BORDERPILOT AI</h1>

      {/* Progress Bar */}
      <div className="flex justify-between mb-10">
        {steps.map((label, index) => {
          const stepNumber = index + 1;
          return (
            <div key={label} className="flex flex-col items-center flex-1">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
                  ${
                    stepNumber < step
                      ? "bg-green-500 text-black"
                      : stepNumber === step
                        ? "bg-blue-500"
                        : "bg-gray-600"
                  }`}
              >
                {stepNumber}
              </div>
              <p className="text-xs mt-2 text-center">{label}</p>
            </div>
          );
        })}
      </div>

      {/* Step 1 */}
      {step === 1 && <UploadForm onSuccess={handleExtractSuccess} />}

      {/* Step 3 */}
      {step === 3 && data && (
        <ConfirmationForm
          extractedData={data}
          onValidated={handleValidationResult} // ✅ ConfirmationForm will pass (result, cleanedData)
        />
      )}

      {/* Step 5 */}
      {step === 5 && result && (
        <div className="bg-gray-800 p-6 rounded-xl">
          <h2 className="text-xl font-semibold mb-4">Validation Result</h2>

          <p className="text-lg font-bold mb-2">
            Status:{" "}
            <span
              className={`${
                result.status === "red"
                  ? "text-red-500"
                  : result.status === "yellow"
                    ? "text-yellow-400"
                    : "text-green-400"
              }`}
            >
              {result.status?.toUpperCase()}
            </span>
          </p>

          {/* VIES Verification Section */}
          {result.vies_verification && (
            <div className="mt-6 bg-gray-700 p-4 rounded-lg text-sm">
              <h3 className="text-md font-semibold mb-3 text-white">
                VAT Verification (VIES)
              </h3>

              {/* Receiver VAT */}
              {result.vies_verification.receiver && (
                <div className="mb-3">
                  <p>
                    <span className="font-semibold">Receiver VAT:</span>{" "}
                    {confirmedData?.receiver_vat || "N/A"} {/* ✅ FIXED */}
                  </p>

                  {result.vies_verification.receiver.error ? (
                    <p className="text-yellow-400">
                      VIES service unavailable – manual verification required.
                    </p>
                  ) : (
                    <>
                      <p>
                        <span className="font-semibold">VIES Status:</span>{" "}
                        {result.vies_verification.receiver.valid ? (
                          <span className="text-green-400">VALID</span>
                        ) : (
                          <span className="text-red-400">INVALID</span>
                        )}
                      </p>

                      {result.vies_verification.receiver.verification_token && (
                        <p className="text-blue-400 break-all">
                          Verification Token:{" "}
                          {result.vies_verification.receiver.verification_token}
                        </p>
                      )}
                    </>
                  )}
                </div>
              )}

              {/* Shipper VAT */}
              {result.vies_verification.shipper && (
                <div>
                  <p>
                    <span className="font-semibold">Shipper VAT:</span>{" "}
                    {confirmedData?.shipper_vat || "N/A"} {/* ✅ FIXED */}
                  </p>

                  {result.vies_verification.shipper.error ? (
                    <p className="text-yellow-400">
                      VIES service unavailable – manual verification required.
                    </p>
                  ) : (
                    <>
                      <p>
                        <span className="font-semibold">VIES Status:</span>{" "}
                        {result.vies_verification.shipper.valid ? (
                          <span className="text-green-400">VALID</span>
                        ) : (
                          <span className="text-red-400">INVALID</span>
                        )}
                      </p>

                      {result.vies_verification.shipper.verification_token && (
                        <p className="text-blue-400 break-all">
                          Verification Token:{" "}
                          {result.vies_verification.shipper.verification_token}
                        </p>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Issues */}
          {result.issues?.length > 0 && (
            <ul className="list-disc pl-5 text-red-400 mt-4">
              {result.issues.map((issue, i) => (
                <li key={i}>{issue}</li>
              ))}
            </ul>
          )}

          {/* Warnings */}
          {result.warnings?.length > 0 && (
            <ul className="list-disc pl-5 text-yellow-400 mt-4">
              {result.warnings.map((warn, i) => (
                <li key={i}>{warn}</li>
              ))}
            </ul>
          )}

          {/* Yellow Banner */}
          {result.notification?.type === "warning" && (
            <div className="mt-6 bg-yellow-600 text-black p-4 rounded-lg font-semibold">
              ⚠ {result.notification.message}
            </div>
          )}

          {/* AI Compliance Report */}
          {result.ai_report && (
            <div className="mt-6 bg-gray-700 p-5 rounded-lg">
              <h3 className="text-lg font-semibold mb-3">
                AI Compliance Assessment
              </h3>
              <p className="text-gray-300 whitespace-pre-line">
                {result.ai_report}
              </p>
            </div>
          )}
        </div>
      )}

      {/* 🔴 Critical Modal (Blocking) */}
      {notification && notification.type === "critical" && (
        <div className="fixed inset-0 flex items-center justify-center bg-black/80 z-50">
          <div className="bg-red-700 text-white p-8 rounded-xl max-w-md w-full shadow-lg">
            <h3 className="text-xl font-bold mb-4">🚨 Shipment Blocked</h3>
            <p className="mb-6">{notification.message}</p>
            <button
              onClick={() => {
                setNotification(null);
                if (retryCount >= 1) {
                  setStep(5);
                } else {
                  setRetryCount((prev) => prev + 1);
                  setStep(3);
                }
              }}
              className="w-full bg-black hover:bg-gray-800 py-2 rounded-lg font-semibold"
            >
              Acknowledge & Recheck
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
