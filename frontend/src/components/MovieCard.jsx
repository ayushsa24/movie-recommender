import React from 'react';


function MovieCard({ title, description, image, rating, director, watch_link }) {
  const imgSrc = image || '/placeholder-movie.png'; 
  const movieTitle = title || 'Untitled';
  const movieDesc = description || 'No description available.';
  const movieDirector = director || 'Unknown';
  const movieRating = rating !== undefined && rating !== null ? rating : 'N/A';
  const link = watch_link || '#';

  return (
    <div className="movie-card">
      <img src={imgSrc} alt={movieTitle} className="movie-image" />
      <h3>{movieTitle}</h3>
      <p>{movieDesc}</p>
      <p><strong>🎬 Director:</strong> {movieDirector}</p>
      <p><strong>⭐ Rating:</strong> {movieRating}</p>
      <a
        href={link}
        target="_blank"
        rel="noopener noreferrer"
        className="watch-button"
      >
        ▶️ Watch Now
      </a>
    </div>
  );
}

export default MovieCard;
