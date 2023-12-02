import React, {useState, useEffect} from 'react'

const App = () => {
  const [textInput, setTextInput] = useState('');
  const [detectionResult, setDetectionResult] = useState(null);

  const handleInputChange = (event) => {
    setTextInput(event.target.value);
  };

  const handleDetectClick = async () => {
    try {
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
  <div className="main-container" style={{ background: 'blue', height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
    <h1 style={{ color: 'white' }}>Cyberbullying Detection System</h1>
    <input
      type="text"
      id="textInput"
      placeholder="Enter text..."
      value={textInput}
      onChange={handleInputChange}
      style={{ width: '45%', margin: '10px', padding: '5px' }}
    />
    <button
      id="detectButton"
      onClick={handleDetectClick}
      style={{ background: 'yellow', padding: '8px', cursor: 'pointer' }}
    >
      Detect
    </button>
  </div>
);

};

export default App;
