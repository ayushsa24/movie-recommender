import { useState } from 'react';
import MovieCard from './components/MovieCard';

function App() {
  const [input, setInput] = useState('');
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState('offline');
  const [errorMsg, setErrorMsg] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setLoading(true);
    setMovies([]);
    setErrorMsg(null);

    try {
      const response = await fetch('http://localhost:8000/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_input: input, mode: mode }),
      });

      const data = await response.json().catch(() => null);

      if (!response.ok || (data && data.detail)) {
        setErrorMsg(data?.detail || `Server error: ${response.status}`);
        setMovies([]);
        return;
      }

      const normalized = (data.recommended_movies || []).map(m => ({
        title: m.title || (typeof m === 'string' ? m : 'Untitled'),
        description: m.description || m.desc || '',
        image: m.image || '',
        rating: m.rating || '',
        director: m.director || '',
        link: m.link || m.watch_link || ''
      }));
      setMovies(normalized);
    } catch (error) {
      setErrorMsg(String(error));
      setMovies([]);
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setMode(mode === 'offline' ? 'online' : 'offline');
  };

  return (
    <div className="app-container">
      <h1 className="glow-heading">🎬 Smart Movie Recommender</h1>

      {/* Toggle Mode */}
      <div className="mode-toggle">
        <span className={`mode-text ${mode === 'online' ? 'active' : ''}`}>
          {mode === 'online' ? '🌐 Online Mode' : '💾 Offline Mode'}
        </span>
        <button onClick={toggleMode} className="toggle-button">
          Switch to {mode === 'online' ? 'Offline' : 'Online'}
        </button>
      </div>

      {/* Search Bar */}
      <form className="glow-form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="e.g. action movies like Avengers"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="glow-input"
        />
        <button type="submit" className="glow-button">🎥 Get Recommendations</button>
      </form>

      {loading && <p className="loading-text">✨ Fetching movie magic...</p>}

      {errorMsg ? (
        <p className="error-text">{errorMsg}</p>
      ) : (
        movies.length > 0 && (
          <div className="results">
            {movies.map((movie, index) => (
              <MovieCard
                key={index}
                title={movie.title}
                description={movie.description}
                image={movie.image}
                rating={movie.rating}
                director={movie.director}
                watch_link={movie.link}
              />
            ))}
          </div>
        )
      )}

    </div>
  );
}

export default App;
