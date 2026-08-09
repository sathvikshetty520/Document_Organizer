import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/api/documents/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload document");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="glass-card">
        <div className="header">
          <div className="logo-icon">📄</div>
          <h1>AI Document Organizer</h1>
          <p>Upload a PDF to automatically categorize it using local AI.</p>
        </div>

        <div className="upload-zone">
          <input 
            type="file" 
            id="file-upload" 
            accept=".pdf" 
            onChange={handleFileChange} 
            className="file-input"
          />
          <label htmlFor="file-upload" className="file-label">
            <span className="upload-icon">📁</span>
            {file ? (
              <span className="filename">{file.name}</span>
            ) : (
              <span className="placeholder">Choose a PDF file or drag it here</span>
            )}
          </label>
        </div>

        <button 
          className={`upload-btn ${loading ? 'loading' : ''} ${!file ? 'disabled' : ''}`}
          onClick={handleUpload}
          disabled={!file || loading}
        >
          {loading ? 'Processing...' : 'Categorize Document'}
        </button>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {result && (
          <div className="result-card">
            <h3>Categorization Complete</h3>
            <div className="result-details">
              <div className="result-item">
                <span className="label">Category:</span>
                <span className="value category-badge">{result.category}</span>
              </div>
              <div className="result-item">
                <span className="label">Confidence:</span>
                <span className="value">{(result.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="result-item">
                <span className="label">Method:</span>
                <span className="value">{result.classification_method === 'ai' ? 'AI' : 'Keyword fallback'}</span>
              </div>
              <div className="result-item">
                <span className="label">Saved to:</span>
                <span className="value path-value">{result.path}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
