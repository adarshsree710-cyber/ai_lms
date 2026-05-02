function StatCard({ label, value, hint }) {
  return (
    <article className="stat-card">
      <p className="stat-label">{label}</p>
      <h3 className="stat-value">{value}</h3>
      <p className="muted-text">{hint}</p>
    </article>
  );
}

export default StatCard;
