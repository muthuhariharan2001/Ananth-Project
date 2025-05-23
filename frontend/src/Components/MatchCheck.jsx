// import React, { useState } from "react";
// import axios from "axios";
// import { Toaster, toast } from "react-hot-toast";
// import "react-toastify/dist/ReactToastify.css";

// const MatchCheck = () => {
//   const [preview1, setPreview1] = useState(null);
//   const [preview2, setPreview2] = useState(null);
//   const [hash1, setHash1] = useState("");
//   const [hash2, setHash2] = useState("");
//   const [actionDisabled, setActionDisabled] = useState(false);

//   const generateHash = async (file) => {
//     const arrayBuffer = await file.arrayBuffer();
//     const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);
//     const hashArray = Array.from(new Uint8Array(hashBuffer));
//     return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
//   };

//   const handleCheck = async () => {
//     setActionDisabled(true);
//     try {
//       const response = await axios.post("http://localhost:8000/check-image-hash/", {
//         hash1,
//         hash2,
//       });

//       const { image1_found, image2_found } = response.data;
//       if (image1_found && image2_found) {
//         toast.success("Both images are found in the database");
//       } 
//       else {
//         toast.error("One or both images are not found in the database");
//       }
//     } catch (error) {
//       toast.error("🚨 Error checking images");
//       console.error(error);
//     } finally {
//       setActionDisabled(false);
//     }
//   };

//   const saveHashToDB = async (hashValue, db) => {
//     try {
//       const res = await axios.post("http://localhost:8000/save-image-hash/", {
//         hash: hashValue,
//         db: db,
//       });

//       if (res.data.status === "saved") {
//         toast.success(`✅ Saved in DB-${db}`, { toastId: `saved-${db}` });
//       } else if (res.data.status === "exists") {
//         toast.info(`ℹAlready exists in DB-${db}`, { toastId: `exists-${db}` });
//       }
//     } catch (error) {
//       toast.error(` Failed to save hash in DB-${db}`, { toastId: `error-${db}` });
//     }
//   };


//   const handleFileChange = async (e, type) => {
//     const file = e.target.files[0];
//     if (!file) return;

//     const hash = await generateHash(file);
//     const preview = URL.createObjectURL(file);

//     if (type === "A") {
//       setHash1(hash);
//       setPreview1(preview);
//     } else {
//       setHash2(hash);
//       setPreview2(preview);
//     }
//   };

//   return (
//     <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200">
//       <div className="w-full max-w-xl p-8 bg-white shadow-xl rounded-xl">
//         <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
//           Upload Two Images for Match Check
//         </h2>

//         {/* Image 1 Input */}
//         <div className="mb-6">
//           <label className="block font-medium text-gray-700 mb-1">Image for DB-A:</label>
//           <input
//             type="file"
//             accept="image/*"
//             onChange={(e) => handleFileChange(e, "A")}
//             className="block w-full border border-gray-300 rounded px-3 py-2"
//           />
//           {preview1 && (
//             <div className="mt-2">
//               <img src={preview1} alt="Preview 1" className="h-40 mx-auto rounded shadow" />
//               <p className="text-xs text-center break-all mt-1">Hash: {hash1}</p>
//             </div>
//           )}
//         </div>

//         {/* Image 2 Input */}
//         <div className="mb-6">
//           <label className="block font-medium text-gray-700 mb-1">Image for DB-B:</label>
//           <input
//             type="file"
//             accept="image/*"
//             onChange={(e) => handleFileChange(e, "B")}
//             className="block w-full border border-gray-300 rounded px-3 py-2"
//           />
//           {preview2 && (
//             <div className="mt-2">
//               <img src={preview2} alt="Preview 2" className="h-40 mx-auto rounded shadow" />
//               <p className="text-xs text-center break-all mt-1">Hash: {hash2}</p>
//             </div>
//           )}
//         </div>

//         <button
//           onClick={handleCheck}
//           disabled={!hash1 || !hash2 || actionDisabled}
//           className={`w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition ${(!hash1 || !hash2 || actionDisabled) && "opacity-50 cursor-not-allowed"
//             }`}
//         >
//           Check Images
//         </button>

//         {/* <ToastContainer
//           position="top-right"
//           autoClose={3000}
//           limit={2}
//           hideProgressBar={false}
//           newestOnTop
//           closeOnClick
//           rtl={false}
//           pauseOnFocusLoss
//           draggable
//           pauseOnHover
//         /> */}

//       </div>
//     </div>
//   );
// };

// export default MatchCheck;

import React, { useState } from "react";
import axios from "axios";
import Tesseract from "tesseract.js";
import { toast, Toaster } from "react-hot-toast";

const MatchCheck = () => {
  const [preview1, setPreview1] = useState(null);
  const [preview2, setPreview2] = useState(null);
  const [hash1, setHash1] = useState("");
  const [hash2, setHash2] = useState("");
  const [actionDisabled, setActionDisabled] = useState(false);
  const [loadingMsg, setLoadingMsg] = useState("");

  const generateHash = async (file) => {
    const arrayBuffer = await file.arrayBuffer();
    const hashBuffer = await crypto.subtle.digest("SHA-256", arrayBuffer);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map((b) => b.toString(16).padStart(2, "0")).join("");
  };

  const runOCR = async (file) => {
    setLoadingMsg("Running OCR...");
    const { data: { text } } = await Tesseract.recognize(file, "eng+tam");
    setLoadingMsg("OCR completed");
    console.log(text);
    
    return text.toLowerCase();
  };

  const validateText = (text, type) => {
    if (type === "A") {
      return text.includes("aadhaar") || text.includes("government") || text.includes("uidai") || text.includes("7555") || text.includes("aadhar") || text.includes("aadhaar card") || text.includes("unique") || text.includes("identification") || text.includes("aadhaar number") || text.includes("authority") || text.includes("of india") || text.includes("identification") || text.includes("Authority") || text.includes("uid");
    } else {
      return text.includes("smart card") || text.includes("government") || text.includes("CHE") || text.includes("PHH") || text.includes("tamil Nadu") || text.includes("sart") || text.includes("smart card") || text.includes("civil") || text.includes("ration") || text.includes("Department") || text.includes("food") || text.includes("supply") || text.includes("Tamil Nadu") || text.includes("ணை") || text.includes("PIBY ");
    }
  };

  const handleFileChange = async (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    const preview = URL.createObjectURL(file);
    type === "A" ? setPreview1(preview) : setPreview2(preview);

    try {
      const ocrText = await runOCR(file);

      if (!validateText(ocrText, type)) {
        // toast.error(`❌ Invalid ${type === "A" ? "Aadhar" : "Smart Card"} content`);
        return;
      }

      const hash = await generateHash(file);
      toast.success(`✅ Valid ${type === "A" ? "Aadhar" : "Smart Card"} detected`);
      // await saveHashToDB(hash, type);
      type === "A" ? setHash1(hash) : setHash2(hash);
    } catch (error) {
      console.error(error);
      // toast.error("❌ OCR processing failed");
    } finally {
      setLoadingMsg("");
    }
  };

  const saveHashToDB = async (hashValue, db) => {
    try {
      const res = await axios.post("http://localhost:8000/save-image-hash/", {
        hash: hashValue,
        db: db,
      });

      // if (res.data.status === "saved") {
      //   // toast.success(`🗃️ Saved in DB-${db}`);
      // } else {
      //   // toast.info(`📦 Already exists in DB-${db}`);
      // }
    } catch (error) {
      toast.error(`Failed to save hash in DB-${db}`);
    }
  };

  const handleCheck = async () => {
    setActionDisabled(true);
    // setLoadingMsg("🔎 Verifying both hashes...");
    try {
      const response = await axios.post("http://localhost:8000/check-image-hash/", {
        hash1,
        hash2,
      });
      console.log(response.data);

      // const { image1_found, image2_found } = response.data;
      if (response.data.message == "Both cards belong to the same person.") {
        toast.success(response.data.message);
      }
      else {
        toast.error(response.data.message);
      }

      
    } catch (error) {
      console.error(error);
      toast.error("Error while checking match");
    } finally {
      setActionDisabled(false);
      setLoadingMsg("");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 to-gray-200">
      <Toaster />
      <div className="w-full max-w-xl p-8 bg-white shadow-xl rounded-xl">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
          Upload Aadhar & Smart Card
        </h2>

        {loadingMsg && <p className="text-center text-blue-600 mb-4">{loadingMsg}</p>}

        {/* Aadhar Image Input */}
        <div className="mb-6">
          <label className="block font-medium text-gray-700 mb-1">Aadhar Card:</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => handleFileChange(e, "A")}
            className="block w-full border border-gray-300 rounded px-3 py-2"
          />
          {preview1 && (
            <div className="mt-2 text-center">
              <img src={preview1} alt="Aadhar Preview" className="h-40 mx-auto rounded shadow" />
              <p className="text-xs mt-1 break-all">Hash: {hash1}</p>
            </div>
          )}
        </div>

        {/* Smart Card Image Input */}
        <div className="mb-6">
          <label className="block font-medium text-gray-700 mb-1">Smart Card:</label>
          <input
            type="file"
            accept="image/*"
            onChange={(e) => handleFileChange(e, "B")}
            className="block w-full border border-gray-300 rounded px-3 py-2"
          />
          {preview2 && (
            <div className="mt-2 text-center">
              <img src={preview2} alt="Smart Card Preview" className="h-40 mx-auto rounded shadow" />
              <p className="text-xs mt-1 break-all">Hash: {hash2}</p>
            </div>
          )}
        </div>

        <button
          onClick={handleCheck}
          disabled={!hash1 || !hash2 || actionDisabled}
          className={`w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition ${
            (!hash1 || !hash2 || actionDisabled) && "opacity-50 cursor-not-allowed"
          }`}
        >
          Check if Both Cards Match
        </button>
      </div>
    </div>
  );
};

export default MatchCheck;
