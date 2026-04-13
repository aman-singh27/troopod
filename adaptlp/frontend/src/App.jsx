import { useState } from 'react';
import { Toaster } from 'react-hot-toast';
import Navbar from './components/Navbar';
import HomePage from './pages/Home';
import ResultPage from './pages/Result';
import './index.css';

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');
  const [result, setResult] = useState(null);

  const handleResultReady = (resultData) => {
    setResult(resultData);
    setCurrentPage('result');
  };

  const handleBackToHome = () => {
    setCurrentPage('home');
    setResult(null);
  };

  return (
    <>
      <Navbar />
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#13131f',
            color: '#ffffff',
            border: '1px solid rgba(124, 58, 237, 0.2)',
            borderRadius: '16px',
          },
        }}
      />
      
      {currentPage === 'home' && <HomePage onResultReady={handleResultReady} />}
      {currentPage === 'result' && result && <ResultPage result={result} onBack={handleBackToHome} />}
    </>
  );
}
