import { useState, useEffect, useRef } from "react"

const API_BASE = "https://quant-vol-engine-production.up.railway.app"

export default function App() {
  const [stockPrice, setStockPrice] = useState(100)
  const [strikePrice, setStrikePrice] = useState(100)
  const [vol, setVol] = useState(0.2)
  const [rfr, setRfr] = useState(0.05)
  const [timeToExpiry, setTimeToExpiry] = useState(1)
  const [kappa, setKappa] = useState(2)
  const [theta, setTheta] = useState(0.04)
  const [xi, setXi] = useState(0.3)
  const [rho, setRho] = useState(-0.7)
  const [v_0, setV_0] = useState(0.04)
  const [option_type, setOptionType] = useState("call")
  const [hestonResult, setHestonResult] = useState(null)
  const [calibrationResults, setCalibrationResult] = useState(null)
  const [numSimulations, setNumSimulations] = useState(10000)
  const [priceResult, setPriceResult] = useState(null)
  const [greeksResult, setGreeksResult] = useState(null)
  const [monteCarloResult, setMonteCarloResult] = useState(null)
  const [ticker, setTicker] = useState("AAPL")
  const [chainResult, setChainResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [surfaceData, setSurfaceData] = useState([])
  const [sviFits, setSviFits] = useState([])
  const surfaceRef = useRef(null)

  const handleSubmit = async () => {
    setLoading(true)
    const body = JSON.stringify({ stockPrice, strikePrice, vol, rfr, timeToExpiry, numSimulations })
    const headers = { "Content-Type": "application/json" }
    const [priceRes, greeksRes, monteCarloRes] = await Promise.all([
      fetch(`${API_BASE}/price`, { method: "POST", headers, body }),
      fetch(`${API_BASE}/greeks`, { method: "POST", headers, body }),
      fetch(`${API_BASE}/monte-carlo`, { method: "POST", headers, body })
    ])
    const [priceData, greeksData, monteCarloData] = await Promise.all([priceRes.json(), greeksRes.json(), monteCarloRes.json()])
    setPriceResult(priceData)
    setGreeksResult(greeksData)
    setMonteCarloResult(monteCarloData)
    setLoading(false)
  }
  const fetchChain = async () => {
    const res = await fetch(`${API_BASE}/chain/${ticker}`)
    const data = await res.json()
    setChainResult(data)
  }

  const fetchVolSurface = async () => {

    const res = await fetch(`${API_BASE}/vol-surface/${ticker}`)
    const data = await res.json()
    setSurfaceData(data.surface)
    setSviFits(data.svi_fits)
  }

  const svi_variance = (k, a, b, rho, m, sigma) => {

    return a + b * (rho * (k - m) + Math.sqrt(((k-m) ** 2) + Math.pow(sigma,2)))
  }
   
  const buildSurfaceGrid = (sviFits, stockPrice) => {
    
    const xGrid = Array.from({length: 50}, (_, i) => -1 + i * 0.04) //x-Grid
    const yGrid = sviFits.map(fit => fit.T)
    const zGrid = sviFits.map(fit => {
                  const [a, b, rho, m, sigma] = fit.params
                  return xGrid.map(k => Math.sqrt(svi_variance(k, a, b, rho, m, sigma)))
                })
    return {x: xGrid, y: yGrid, z: zGrid}

  }

  useEffect(() => {
              if (surfaceData.length > 0 && surfaceRef.current) {
                const {x, y, z} = buildSurfaceGrid(sviFits, stockPrice)
                window.Plotly.react(surfaceRef.current, [{
                  type: 'surface',
                  x: x,
                  y: y,
                  z: z,
                }], {
                  title: 'Implied Vol Surface',
                  width: 700,
                  height: 500,
                  paper_bgcolor: '#0f172a',
                  font: { color: '#e2e8f0' }
                })
              }
            }, [surfaceData, sviFits])

  const fmt = (n) => n?.toFixed(4)

  const inputs = [
    { label: "Stock Price (S)", value: stockPrice, set: setStockPrice, step: 1 },
    { label: "Strike Price (K)", value: strikePrice, set: setStrikePrice, step: 1 },
    { label: "Volatility (σ)", value: vol, set: setVol, step: 0.01 },
    { label: "Risk Free Rate (r)", value: rfr, set: setRfr, step: 0.01 },
    { label: "Time to Expiry (T)", value: timeToExpiry, set: setTimeToExpiry, step: 0.01 },
    { label: "Simulations", value: numSimulations, set: setNumSimulations, step: 1000 },
    { label: "Kappa (κ)", value: kappa, set: setKappa, step: 1 },
    { label: "Theta (θ)", value: theta, set: setTheta, step: 0.001 },
    { label: "Xi (ξ)", value: xi, set: setXi, step: 1 },
    { label: "Rho (ρ)", value: rho, set: setRho, step: 0.01 },
    { label: "Initial Volatility (v_0)", value: v_0, set: setV_0, step: 0.01 },    
  ]

  const fetchHeston = async () => {
    
    const body = JSON.stringify({ stockPrice, strikePrice, timeToExpiry, rfr, kappa, theta, xi, rho, v_0, option_type })
    const headers = { "Content-Type": "application/json" }

    const hestonRes = await fetch(`${API_BASE}/heston`, { method: "POST", headers, body })
    const hestonData = await hestonRes.json() 

    setHestonResult(hestonData)
  }

  const fetchCalibration = async () => {

    const calibrationRes = await fetch(`${API_BASE}/heston-calibrate/${ticker}`)
    const data = await calibrationRes.json()
    setCalibrationResult(data)
  }


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

          <button
            onClick={fetchVolSurface}
            style={{ width: "100%", marginTop: "0.5rem", background: "#0369a1", border: "none", borderRadius: "4px", color: "#e0f2fe", padding: "0.75rem", fontSize: "0.8rem", fontFamily: "inherit", letterSpacing: "0.1em", textTransform: "uppercase", cursor: "pointer" }}
          >
            {loading ? "Creating Vol Surface..." : "▶ Get Vol Surface"}
          </button>

          <input
            type="text"
            value={option_type}
            onChange={(e) => setOptionType(e.target.value)}
            placeholder="call or put"
            style={{ width: "100%", background: "#1e293b", border: "1px solid #1e3a5f", borderRadius: "4px", color: "#38bdf8", padding: "0.5rem 0.75rem", fontSize: "0.9rem", fontFamily: "inherit", boxSizing: "border-box", marginTop: "1rem" }}
          />

          <button
            onClick={fetchHeston}
            style={{ width: "100%", marginTop: "0.5rem", background: "#0369a1", border: "none", borderRadius: "4px", color: "#e0f2fe", padding: "0.75rem", fontSize: "0.8rem", fontFamily: "inherit", letterSpacing: "0.1em", textTransform: "uppercase", cursor: "pointer" }}
          >
            {loading ? "Getting Heston Price..." : "▶ Get Heston Model Value"}
          </button>

          <button
            onClick={fetchCalibration}
            style={{ width: "100%", marginTop: "0.5rem", background: "#0369a1", border: "none", borderRadius: "4px", color: "#e0f2fe", padding: "0.75rem", fontSize: "0.8rem", fontFamily: "inherit", letterSpacing: "0.1em", textTransform: "uppercase", cursor: "pointer" }}
          >
            {loading ? "Calibrating Heston..." : "▶ Calibrate Heston"}
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
          {surfaceData.length > 0 && <div ref={surfaceRef} />}

          {hestonResult && (
            <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
              <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>▸ Heston Model Price</p>
              <div style={{ background: "#1e293b", borderRadius: "6px", padding: "1rem" }}>
                <p style={{ fontSize: "0.65rem", color: "#64748b", marginBottom: "0.25rem", letterSpacing: "0.1em" }}>Option Price</p>
                <p style={{ fontSize: "1.4rem", color: "#38bdf8", fontWeight: 700 }}>${fmt(hestonResult)}</p>
              </div>
            </div>
          )}
          {calibrationResults && (
            <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
              <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>▸ Calibrated Heston Parameters</p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                {[["Kappa (κ)", 0], ["Theta (θ)", 1], ["Xi (ξ)", 2], ["Rho (ρ)", 3], ["v₀", 4]].map(([label, idx]) => (
                  <div key={label} style={{ background: "#1e293b", borderRadius: "6px", padding: "0.75rem" }}>
                    <p style={{ fontSize: "0.6rem", color: "#64748b", marginBottom: "0.2rem" }}>{label}</p>
                    <p style={{ fontSize: "0.95rem", color: "#38bdf8", fontWeight: 600 }}>{fmt(calibrationResults[idx])}</p>
                  </div>
                ))}
              </div>
            </div>
          )}



        </div>
      </div>
    </div>
  )
}