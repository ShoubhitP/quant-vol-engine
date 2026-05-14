import { useState } from "react"

export default function App() {
  const [stockPrice, setStockPrice] = useState(100)
  const [strikePrice, setStrikePrice] = useState(100)
  const [vol, setVol] = useState(0.2)
  const [rfr, setRfr] = useState(0.05)
  const [timeToExpiry, setTimeToExpiry] = useState(1)
  const [numSimulations, setNumSimulations] = useState(10000)
  const [priceResult, setPriceResult] = useState(null)
  const [greeksResult, setGreeksResult] = useState(null)
  const [monteCarloResult, setMonteCarloResult] = useState(null)
  const [ticker, setTicker] = useState("AAPL")
  const [chainResult, setChainResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    const body = JSON.stringify({ stockPrice, strikePrice, vol, rfr, timeToExpiry, numSimulations })
    const headers = { "Content-Type": "application/json" }
    const [priceRes, greeksRes, monteCarloRes] = await Promise.all([
      fetch(" https://quant-vol-engine-production.up.railway.app/price", { method: "POST", headers, body }),
      fetch(" https://quant-vol-engine-production.up.railway.app/greeks", { method: "POST", headers, body }),
      fetch(" https://quant-vol-engine-production.up.railway.app/monte-carlo", { method: "POST", headers, body })
    ])
    const [priceData, greeksData, monteCarloData] = await Promise.all([priceRes.json(), greeksRes.json(), monteCarloRes.json()])
    setPriceResult(priceData)
    setGreeksResult(greeksData)
    setMonteCarloResult(monteCarloData)
    setLoading(false)
  }

  const fetchChain = async () => {
    const res = await fetch(` https://quant-vol-engine-production.up.railway.app/chain/${ticker}`)
    const data = await res.json()
    setChainResult(data)
  }

  const fmt = (n) => n?.toFixed(4)

  const inputs = [
    { label: "Stock Price (S)", value: stockPrice, set: setStockPrice, step: 1 },
    { label: "Strike Price (K)", value: strikePrice, set: setStrikePrice, step: 1 },
    { label: "Volatility (σ)", value: vol, set: setVol, step: 0.01 },
    { label: "Risk Free Rate (r)", value: rfr, set: setRfr, step: 0.01 },
    { label: "Time to Expiry (T)", value: timeToExpiry, set: setTimeToExpiry, step: 0.01 },
    { label: "Simulations", value: numSimulations, set: setNumSimulations, step: 1000 },
  ]

  //console.log("monteCarloResult state:", monteCarloResult)

  return (
    <div style={{ minHeight: "100vh", background: "#0a0a0f", color: "#e2e8f0", fontFamily: "'JetBrains Mono', 'Fira Code', monospace", padding: "2rem" }}>
      <h1 style={{ fontSize: "1.5rem", fontWeight: 700, letterSpacing: "0.1em", color: "#38bdf8", marginBottom: "0.25rem", textTransform: "uppercase" }}>
        ⬡ Quant Vol Engine
      </h1>
      <p style={{ fontSize: "0.75rem", color: "#475569", marginBottom: "2rem", letterSpacing: "0.05em" }}>
        Black-Scholes Pricing · Monte Carlo · Greeks Analytics
      </p>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1.5rem" }}>
        <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
          <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1.25rem" }}>
            ▸ Parameters
          </p>
          {inputs.map(({ label, value, set, step }) => (
            <div key={label} style={{ marginBottom: "1rem" }}>
              <label style={{ fontSize: "0.7rem", color: "#64748b", letterSpacing: "0.1em", display: "block", marginBottom: "0.35rem" }}>
                {label}
              </label>
              <input
                type="number"
                value={value}
                step={step}
                onChange={(e) => set(Number(e.target.value))}
                style={{ width: "100%", background: "#1e293b", border: "1px solid #1e3a5f", borderRadius: "4px", color: "#38bdf8", padding: "0.5rem 0.75rem", fontSize: "0.9rem", fontFamily: "inherit", boxSizing: "border-box" }}
              />
            </div>
          ))}

          <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value.toUpperCase())}
              placeholder="AAPL"
              style={{ width: "100%", background: "#1e293b", border: "1px solid #1e3a5f", borderRadius: "4px", color: "#38bdf8", padding: "0.5rem 0.75rem", fontSize: "0.9rem", fontFamily: "inherit", boxSizing: "border-box", marginTop: "1rem" }}
          />
          <button
            onClick={handleSubmit}
            style={{ width: "100%", marginTop: "0.5rem", background: "#0369a1", border: "none", borderRadius: "4px", color: "#e0f2fe", padding: "0.75rem", fontSize: "0.8rem", fontFamily: "inherit", letterSpacing: "0.1em", textTransform: "uppercase", cursor: "pointer" }}
          >
            {loading ? "Computing..." : "▶ Calculate"}
          </button>

          <button
            onClick={fetchChain}
            style={{ width: "100%", marginTop: "0.5rem", background: "#0369a1", border: "none", borderRadius: "4px", color: "#e0f2fe", padding: "0.75rem", fontSize: "0.8rem", fontFamily: "inherit", letterSpacing: "0.1em", textTransform: "uppercase", cursor: "pointer" }}
          >
            {loading ? "Getting Option Chain..." : "▶ Get Stock Option Chain"}
          </button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {priceResult && (
            <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
              <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>▸ Prices</p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
                {[["Call Price", priceResult["Call Price"]], ["Put Price", priceResult["Put Price"]]].map(([label, val]) => (
                  <div key={label} style={{ background: "#1e293b", borderRadius: "6px", padding: "1rem" }}>
                    <p style={{ fontSize: "0.65rem", color: "#64748b", marginBottom: "0.25rem", letterSpacing: "0.1em" }}>{label}</p>
                    <p style={{ fontSize: "1.4rem", color: "#38bdf8", fontWeight: 700 }}>${fmt(val)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {greeksResult && (
            <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
              <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>▸ Greeks</p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                {[
                  ["Delta (Call)", greeksResult["Delta Call"]],
                  ["Delta (Put)", greeksResult["Delta Put"]],
                  ["Gamma", greeksResult["Gamma Value"]],
                  ["Vega", greeksResult["Vega Value"]],
                  ["Theta (Call)", greeksResult["Theta Call"]],
                  ["Theta (Put)", greeksResult["Theta Put"]],
                  ["Rho (Call)", greeksResult["Rho Call"]],
                  ["Rho (Put)", greeksResult["Rho Put"]],
                  ["Vanna", greeksResult["Vanna Value"]],
                  ["Volga", greeksResult["Volga Value"]],
                  ["Zomma", greeksResult["Zomma Value"]],
                ].map(([label, val]) => (
                  <div key={label} style={{ background: "#1e293b", borderRadius: "6px", padding: "0.75rem" }}>
                    <p style={{ fontSize: "0.6rem", color: "#64748b", marginBottom: "0.2rem", letterSpacing: "0.08em" }}>{label}</p>
                    <p style={{ fontSize: "0.95rem", color: val < 0 ? "#f87171" : "#34d399", fontWeight: 600 }}>{fmt(val)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {monteCarloResult && (
            <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
              <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>▸ Monte Carlo</p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "0.75rem" }}>
                {[
                  ["Monte Carlo", monteCarloResult["Monte Carlo Value"]],
                  ["Lower Bound", monteCarloResult["Lower Bound"]],
                  ["Upper Bound", monteCarloResult["Upper Bound"]],
                ].map(([label, val]) => (
                  <div key={label} style={{ background: "#1e293b", borderRadius: "6px", padding: "0.75rem" }}>
                    <p style={{ fontSize: "0.6rem", color: "#64748b", marginBottom: "0.2rem", letterSpacing: "0.08em" }}>{label}</p>
                    <p style={{ fontSize: "0.95rem", color: "#38bdf8", fontWeight: 600 }}>${fmt(val)}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {chainResult && (
            <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
              <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>▸ Options Chain — {ticker}</p>
              <p style={{ fontSize: "0.65rem", color: "#64748b", marginBottom: "0.5rem" }}>CALLS</p>
              <table style={{ width: "100%", fontSize: "0.7rem", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ color: "#64748b" }}>
                    <th style={{ textAlign: "left", padding: "4px" }}>Strike</th>
                    <th style={{ textAlign: "left", padding: "4px" }}>Bid</th>
                    <th style={{ textAlign: "left", padding: "4px" }}>Ask</th>
                    <th style={{ textAlign: "left", padding: "4px" }}>IV</th>
                    <th style={{ textAlign: "left", padding: "4px" }}>OI</th>
                  </tr>
                </thead>
                <tbody>
                  {chainResult["Calls"].slice(0, 10).map((row, i) => (
                    <tr key={i} style={{ color: row.inTheMoney ? "#34d399" : "#e2e8f0", borderTop: "1px solid #1e3a5f" }}>
                      <td style={{ padding: "4px" }}>{row.strike}</td>
                      <td style={{ padding: "4px" }}>{row.bid}</td>
                      <td style={{ padding: "4px" }}>{row.ask}</td>
                      <td style={{ padding: "4px" }}>{(row.impliedVolatility * 100).toFixed(1)}%</td>
                      <td style={{ padding: "4px" }}>{row.openInterest}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}