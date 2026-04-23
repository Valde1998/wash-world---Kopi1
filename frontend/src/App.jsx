import { useState, useEffect } from 'react';
import { login, logout, getMe } from './services/api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await getMe();
      setUser(response.data);
    } catch (error) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await login(username, password);
      checkAuth();
      setUsername('');
      setPassword('');
    } catch (error) {
      alert('Login fejlede: ' + (error.response?.data?.error || error.message));
    }
  };

  const handleLogout = async () => {
    await logout();
    setUser(null);
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="app">
      <h1>🧼 Wash World</h1>
      
      {!user ? (
        <form onSubmit={handleLogin} className="login-form">
          <h2>Log ind</h2>
          <input
            type="text"
            placeholder="Brugernavn"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <input
            type="password"
            placeholder="Adgangskode"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <button type="submit">Log ind</button>
          <p>
            Har du ikke en bruger? <a href="#" onClick={() => alert('Opret bruger kommer snart!')}>Opret her</a>
          </p>
        </form>
      ) : (
        <div className="dashboard">
          <div className="header">
            <p>Velkommen, <strong>{user.username}</strong>!</p>
            <button onClick={handleLogout} className="logout-btn">Log ud</button>
          </div>
          <div className="content">
            <h2>Dine vaskereservationer</h2>
            <p>Her kommer listen over bookings...</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;