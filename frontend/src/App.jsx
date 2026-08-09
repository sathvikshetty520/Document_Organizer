import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState(null);
  const [searchError, setSearchError] = useState(null);

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

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    setSearchError(null);
    setSearchResults(null);

    try {
      const response = await fetch(`http://localhost:8000/api/documents/search?q=${encodeURIComponent(searchQuery)}`);
      if (!response.ok) {
        throw new Error("Search failed");
      }
      const data = await response.json();
      setSearchResults(data.results);
    } catch (err) {
      setSearchError("Unable to search documents. Please try again.");
    } finally {
      setIsSearching(false);
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
            <h3>✕ Document processing failed</h3>
            <p>Unable to organize the document.</p>
            <p className="error-details">{error}</p>
          </div>
        )}

        {result && (
          <div className="result-card">
            <h3>✓ Document Organized</h3>
            
            <div className="result-filename">
              📄 {result.filename}
            </div>

            <div className="result-details">
              <div className="result-item">
                <span className="label">Category</span>
                <span className="value category-badge">{result.category}</span>
              </div>
              <div className="result-item">
                <span className="label">Confidence</span>
                <span className="value">{(result.confidence * 100).toFixed(0)}%</span>
              </div>
              <div className="result-item">
                <span className="label">Method</span>
                <span className="value">{result.classification_method === 'ai' ? 'AI Classification' : 'Keyword Fallback'}</span>
              </div>
            </div>

            <div className="result-destination">
              <div className="dest-title">📁 Organized into</div>
              <div className="dest-row">
                <div className="dest-category">{result.category}</div>
                <div className="dest-path">{result.path}</div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="glass-card search-card">
        <div className="header">
          <h2>🔎 Search Your Documents</h2>
        </div>
        
        <form className="search-form" onSubmit={handleSearch}>
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="e.g. bank statements"
            className="search-input"
          />
          <button type="submit" className="search-btn" disabled={isSearching || !searchQuery.trim()}>
            {isSearching ? 'Searching...' : 'Search'}
          </button>
        </form>

        {searchError && (
          <div className="error-message">
            ⚠️ {searchError}
          </div>
        )}

        {searchResults && (
          <div className="search-results">
            <h3>Search Results</h3>
            {searchResults.length === 0 ? (
              <p className="no-results">No matching documents found.</p>
            ) : (
              <div className="results-list">
                {searchResults.map((doc, idx) => (
                  <div key={idx} className="result-card search-result-item">
                    <div className="result-filename">📄 {doc.filename}</div>
                    <div className="result-details">
                      <div className="result-item">
                        <span className="label">Category</span>
                        <span className="value category-badge">{doc.category}</span>
                      </div>
                      <div className="result-item">
                        <span className="label">Match</span>
                        <span className="value">{(doc.score * 100).toFixed(0)}%</span>
                      </div>
                    </div>
                    <div className="result-destination">
                      <div className="dest-path search-dest-path">{doc.path}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

    </div>
  );
}

export default App;
