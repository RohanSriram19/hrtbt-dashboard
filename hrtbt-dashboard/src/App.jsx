import { useState, useEffect } from "react";

function App() {
  const [streamer, setStreamer] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [messages, setMessages] = useState([]);
  const [emotionCounts, setEmotionCounts] = useState({});

  useEffect(() => {
    let interval;
    if (submitted) {
      fetch(`http://127.0.0.1:5000/start?channel=${streamer}&token=oauth:YOUR_TOKEN_HERE`)
        .then(() => {
          interval = setInterval(() => {
            fetch("http://127.0.0.1:5000/messages")
              .then((res) => res.json())
              .then((data) => setMessages(data));

            fetch("http://127.0.0.1:5000/summary")
              .then((res) => res.json())
              .then((data) => setEmotionCounts(data));
          }, 2000);
        });
    }
    return () => clearInterval(interval);
  }, [submitted, streamer]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (streamer.trim()) {
      setSubmitted(true);
      setMessages([]);
      setEmotionCounts({});
    }
  };

  return (
    <div className="min-h-screen p-8 bg-[#0e0e10] text-white font-sans">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Twitch Chat Sentiment Dashboard
      </h1>
      <form onSubmit={handleSubmit} className="flex justify-center mb-8">
        <input
          type="text"
          placeholder="Enter streamer username"
          value={streamer}
          onChange={(e) => setStreamer(e.target.value)}
          className="p-2 text-black rounded-l-md"
        />
        <button type="submit" className="bg-purple-600 px-4 py-2 rounded-r-md hover:bg-purple-700">
          Search
        </button>
      </form>

      {submitted && (
        <>
          <p className="text-center mb-4">🔍 Tracking: <strong>{streamer}</strong></p>

          <div className="grid grid-cols-2 gap-8">
            <div>
              <h2 className="text-xl font-semibold mb-2">Recent Messages</h2>
              <ul className="bg-gray-800 p-4 rounded-md max-h-96 overflow-y-scroll">
                {messages.map((msg, idx) => (
                  <li key={idx} className="mb-2">
                    <span className="text-purple-400 font-semibold">{msg.user}:</span> {msg.text}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h2 className="text-xl font-semibold mb-2">Live Emotion Counts</h2>
              <ul className="bg-gray-800 p-4 rounded-md">
                {Object.entries(emotionCounts).map(([emotion, count]) => (
                  <li key={emotion} className="mb-2 capitalize">
                    {emotion}: {count}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
