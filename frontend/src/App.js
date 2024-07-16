import React, { useState } from 'react';

const App = () => {
  const [textInput, setTextInput] = useState('');
  const [detectionResult, setDetectionResult] = useState(null);

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleDetectClick = async () => {
    try {
      // Split input into words and count words
      const words = textInput.trim().split(/\s+/);
      if (words.length < 2) {
        alert('Please enter at least two words.');
        return;
      }

      const response = await fetch('/test-model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: textInput }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      alert('Cyberbullying detection result: ' + result.result);
      setDetectionResult(result.result);
    } catch (error) {
      console.error('Error sending data to the backend:', error);
      alert('Error sending data to the backend. Please try again.');
    }
  };

  return (
    <div className="main-container" style={{ background: '#007BFF', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
      <h1 style={{ color: 'white', marginBottom: '30px' }}>Cyberbullying Detection System</h1>
      <input
        type="text"
        id="textInput"
        placeholder="Enter text..."
        value={textInput}
        onChange={handleInputChange}
        style={{ width: '60%', maxWidth: '400px', margin: '10px', padding: '12px', fontSize: '16px', border: 'none', borderRadius: '4px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}
      />
      <button
        id="detectButton"
        onClick={handleDetectClick}
        style={{ background: '#FFC107', padding: '12px 24px', cursor: 'pointer', border: 'none', borderRadius: '4px', fontSize: '16px', boxShadow: '0 4px 8px rgba(0,0,0,0.1)', transition: 'background-color 0.3s ease' }}
      >
        Detect
      </button>
      {detectionResult && (
        <p style={{ marginTop: '20px', fontSize: '18px', color: 'white' }}>
          Detection Result: {detectionResult}
        </p>
      )}
    </div>
  );
};

export default App;
