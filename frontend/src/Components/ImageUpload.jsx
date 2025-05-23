import React from "react";
import { Toaster, toast } from "react-hot-toast";

import { useState } from "react";
import axios from "axios";
import "./ImageUpload.css";

function ImageUpload() {
  const [aadhar, setAadhar] = useState(null);
  const [smartCard, setSmartCard] = useState(null);
  const [result, setResult] = useState(null);
  const [aadharPreview, setAadharPreview] = useState(null);
  const [smartCardPreview, setSmartCardPreview] = useState(null);

  const handleFileChange = (e, type) => {
    const file = e.target.files[0];
    if (file) {
      setResult(null); // Clear old results when a new file is selected
      if (type === "aadhar") {
        setAadhar(file);
        setAadharPreview(URL.createObjectURL(file));
      } else {
        setSmartCard(file);
        setSmartCardPreview(URL.createObjectURL(file));
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!aadhar || !smartCard) {
      alert("Please upload both images");
      return;
    }

    const formData = new FormData();
    formData.append("aadhar", aadhar);
    formData.append("smart_card", smartCard);

    try {
      setResult(null);
      const response = await axios.post(
        "http://localhost:8000/upload/",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );
      setResult(response.data);
      toast.success("Files uploaded successfully!");
    } catch (error) {
      if (error.response && error.response.status === 400) {
        const errorMessage = error.response.data?.error || "Bad Request. Try to upload Valid Files.";
        toast.error(errorMessage);
      } else {
        toast.error("Something went wrong. Please try again later.");
      }
    }
  };

  return (
    <div className="container">
      <Toaster />
      <h2>Upload Aadhar & Smart Card</h2>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => handleFileChange(e, "aadhar")}
          />
          {aadharPreview && (
            <img src={aadharPreview} alt="Aadhar Preview" width="200" />
          )}
        </div>

        <div className="input-group">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => handleFileChange(e, "smart_card")}
          />
          {smartCardPreview && (
            <img src={smartCardPreview} alt="Smart Card Preview" width="200" />
          )}
        </div>

        <button type="submit">Submit</button>
        {/* Reset Button */}
        <button
          type="button"
          onClick={() => {
            setAadhar(null);
            setSmartCard(null);
            setResult(null);
            setAadharPreview(null);
            setSmartCardPreview(null);
          }}
        >
          Reset
        </button>
      </form>
      
{/* If result gets its data, an toast has to pop up, 
and then it has to show, if the percentage is greater than 50,
 it has to show, both of the card belongs to the same person */}
      {result && result.match_percentage > 50 && (
        toast.success("Both cards belong to the same person!")
      )}

      {result && (
        <div className="results">
          <h3>Results:</h3>
          <img 
            src={`http://localhost:8000/${
              result.aadhar_image_url
            }?t=${Date.now()}`}
            alt="Uploaded Aadhar"
            width="200"
            className="inline"
          />
          <img
            src={`http://localhost:8000/${
              result.smart_card_image_url
            }?t=${Date.now()}`}
            alt="Uploaded Smart Card"
            width="200"
            className="inline"
          />
          <p>
            <b>Aadhar Number:</b> {result.aadhar_number}
          </p>
          <p>
            <b>Match Percentage:</b> {result.match_percentage}%
          </p>
          <p>
            <b>Aadhar Extracted Text:</b> {result.aadhar_text}
          </p>
          <p>
            <b>Smart Card Extracted Text:</b> {result.smart_card_text}
          </p>
          <p>
            <b>Aadhar Address: </b> {result.aadhar_address}{" "}
          </p>
          <p>
            <b>Smart Card Address: </b> {result.smart_card_address}{" "}
          </p>
          <p>
            <b>Address Match Percentage: </b> {result.address_match_percentage}{" "}
          </p>
        </div>
      )}
    </div>
  );
}

export default ImageUpload;
