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
  const [fdResult, setFdResult] = useState(null)
  const [volComparison, setVolComparison] = useState(null)

  const fmt = (n) => Number(n)?.toFixed(4)

  const handleSubmit = async () => {
    setLoading(true)
    const body = JSON.stringify({ stockPrice, strikePrice, vol, rfr, timeToExpiry, numSimulations })
    const headers = { "Content-Type": "application/json" }

    const [priceRes, greeksRes, monteCarloRes] = await Promise.all([
      fetch(`${API_BASE}/price`, { method: "POST", headers, body }),
      fetch(`${API_BASE}/greeks`, { method: "POST", headers, body }),
      fetch(`${API_BASE}/monte-carlo`, { method: "POST", headers, body }),
    ])

    const [priceData, greeksData, monteCarloData] = await Promise.all([
      priceRes.json(),
      greeksRes.json(),
      monteCarloRes.json(),
    ])

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
    setSurfaceData(data.surface || [])
    setSviFits(data.svi_fits || [])
  }

  const svi_variance = (k, a, b, rho, m, sigma) => {
    return a + b * (rho * (k - m) + Math.sqrt((k - m) ** 2 + sigma ** 2))
  }

  const buildSurfaceGrid = (sviFits) => {
    if (!sviFits || sviFits.length === 0) {
      return { x: [], y: [], z: [] }
    }

    const xGrid = Array.from({ length: 50 }, (_, i) => -0.75 + i * (1.5 / 49))
    const yGrid = sviFits.map(fit => fit.T)

    const zGrid = sviFits.map(fit => {
      const [a, b, rho, m, sigma] = fit.params
      const T = fit.T

      return xGrid.map(k => {
        const variance = svi_variance(k, a, b, rho, m, sigma)

        if (!Number.isFinite(variance) || variance <= 0 || variance > 4 || T <= 0) {
          return null
        }

        const impliedVol = Math.sqrt(variance / T)

        if (!Number.isFinite(impliedVol) || impliedVol > 1.5) {
          return null
        }

        return impliedVol
      })
    })

    return { x: xGrid, y: yGrid, z: zGrid }
  }

  useEffect(() => {
    if (surfaceData.length > 0 && sviFits.length > 0 && surfaceRef.current) {
      const { x, y, z } = buildSurfaceGrid(sviFits)

      window.Plotly.react(
        surfaceRef.current,
        [
          {
            type: "surface",
            x,
            y,
            z,
            colorscale: "Viridis",
            connectgaps: false,
          },
        ],
        {
          title: "SVI Implied Volatility Surface",
          width: 700,
          height: 500,
          paper_bgcolor: "#0f172a",
          plot_bgcolor: "#0f172a",
          font: { color: "#e2e8f0" },
          scene: {
            xaxis: { title: "Log-Moneyness" },
            yaxis: { title: "Time to Expiry" },
            zaxis: { title: "Implied Volatility" },
          },
        }
      )
    }
  }, [surfaceData, sviFits])

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

  const fetchFD = async () => {
    const body = JSON.stringify({ stockPrice, strikePrice, vol, rfr, timeToExpiry })
    const headers = { "Content-Type": "application/json" }
    const res = await fetch(`${API_BASE}/fd`, { method: "POST", headers, body })
    const data = await res.json()
    setFdResult(data)
  }

  const fetchVolComparison = async () => {
    const res = await fetch(`${API_BASE}/vol-comparison/${ticker}`)
    const data = await res.json()
    setVolComparison(data)
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

          <button onClick={handleSubmit} style={buttonStyle}>
            {loading ? "Computing..." : "▶ Calculate"}
          </button>

          <button onClick={fetchChain} style={buttonStyle}>
            ▶ Get Stock Option Chain
          </button>

          <button onClick={fetchVolSurface} style={buttonStyle}>
            ▶ Get Vol Surface
          </button>

          <input
            type="text"
            value={option_type}
            onChange={(e) => setOptionType(e.target.value)}
            placeholder="call or put"
            style={{ width: "100%", background: "#1e293b", border: "1px solid #1e3a5f", borderRadius: "4px", color: "#38bdf8", padding: "0.5rem 0.75rem", fontSize: "0.9rem", fontFamily: "inherit", boxSizing: "border-box", marginTop: "1rem" }}
          />

          <button onClick={fetchHeston} style={buttonStyle}>
            ▶ Get Heston Model Value
          </button>

          <button onClick={fetchCalibration} style={buttonStyle}>
            ▶ Calibrate Heston
          </button>

          <button onClick={fetchFD} style={buttonStyle}>
            ▶ Get FD Prices
          </button>

          <button onClick={fetchVolComparison} style={buttonStyle}>
            ▶ Get Vol Comparison
          </button>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
          {priceResult && (
            <Card title="▸ Prices">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
                {[["Call Price", priceResult["Call Price"]], ["Put Price", priceResult["Put Price"]]].map(([label, val]) => (
                  <Metric key={label} label={label} value={`$${fmt(val)}`} />
                ))}
              </div>
            </Card>
          )}

          {greeksResult && (
            <Card title="▸ Greeks">
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
                  <Metric key={label} label={label} value={fmt(val)} color={val < 0 ? "#f87171" : "#34d399"} />
                ))}
              </div>
            </Card>
          )}

          {monteCarloResult && (
            <Card title="▸ Monte Carlo">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "0.75rem" }}>
                {[
                  ["Monte Carlo", monteCarloResult["Monte Carlo Value"]],
                  ["Lower Bound", monteCarloResult["Lower Bound"]],
                  ["Upper Bound", monteCarloResult["Upper Bound"]],
                ].map(([label, val]) => (
                  <Metric key={label} label={label} value={`$${fmt(val)}`} />
                ))}
              </div>
            </Card>
          )}

          {chainResult && (
            <Card title={`▸ Options Chain — ${ticker}`}>
              <p style={{ fontSize: "0.65rem", color: "#64748b", marginBottom: "0.5rem" }}>CALLS</p>
              <table style={{ width: "100%", fontSize: "0.7rem", borderCollapse: "collapse" }}>
                <thead>
                  <tr style={{ color: "#64748b" }}>
                    <th style={thStyle}>Strike</th>
                    <th style={thStyle}>Bid</th>
                    <th style={thStyle}>Ask</th>
                    <th style={thStyle}>IV</th>
                    <th style={thStyle}>OI</th>
                  </tr>
                </thead>
                <tbody>
                  {chainResult["Calls"].slice(0, 10).map((row, i) => (
                    <tr key={i} style={{ color: row.inTheMoney ? "#34d399" : "#e2e8f0", borderTop: "1px solid #1e3a5f" }}>
                      <td style={tdStyle}>{row.strike}</td>
                      <td style={tdStyle}>{row.bid}</td>
                      <td style={tdStyle}>{row.ask}</td>
                      <td style={tdStyle}>{(row.impliedVolatility * 100).toFixed(1)}%</td>
                      <td style={tdStyle}>{row.openInterest}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </Card>
          )}

          {surfaceData.length > 0 && <div ref={surfaceRef} />}

          {hestonResult && (
            <Card title="▸ Heston Model Price">
              <Metric label="Option Price" value={`$${fmt(hestonResult)}`} large />
            </Card>
          )}

          {calibrationResults && (
            <Card title="▸ Calibrated Heston Parameters">
              {calibrationResults.error ? (
                <p style={{ color: "#f87171", fontSize: "0.8rem" }}>{calibrationResults.error}</p>
              ) : (
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                  {[
                    ["Kappa (κ)", calibrationResults.kappa],
                    ["Theta (θ)", calibrationResults.theta],
                    ["Xi (ξ)", calibrationResults.xi],
                    ["Rho (ρ)", calibrationResults.rho],
                    ["v₀", calibrationResults.v0],
                    ["Contracts Used", calibrationResults.contracts_used],
                  ].map(([label, val]) => (
                    <Metric key={label} label={label} value={fmt(val)} />
                  ))}
                </div>
              )}
            </Card>
          )}

          {fdResult && (
            <Card title="▸ Finite Difference Prices">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                {[
                  ["Explicit FD", fdResult["FD Explicit Price"]],
                  ["Implicit FD", fdResult["FD Implicit Price"]],
                  ["Crank-Nicolson", fdResult["FD Crank-Nicolson Price"]],
                  ["American Put (CN)", fdResult["FD Crank-Nicolson Price For American Put Options"]],
                ].map(([label, val]) => (
                  <Metric key={label} label={label} value={`$${fmt(val)}`} />
                ))}
              </div>
            </Card>
          )}

          {volComparison && (
            <Card title="▸ Volatility Comparison">
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
                {[
                  ["ATM IV", volComparison.atm_iv],
                  ["GARCH 30d", volComparison.garch_30d_forecast],
                  ["30d Realized", volComparison.latest_30d_realized_vol],
                  ["ATM IV - GARCH", volComparison.iv_minus_garch],
                  ["ATM IV - Realized", volComparison.iv_minus_realized],
                ].map(([label, val]) => (
                  <Metric key={label} label={label} value={`${(val * 100).toFixed(2)}%`} />
                ))}
              </div>

              <p style={{ fontSize: "0.75rem", color: "#94a3b8", marginTop: "1rem", lineHeight: 1.6 }}>
                {volComparison.iv_minus_garch > 0
                  ? "Options-implied volatility is above the GARCH forecast."
                  : "Options-implied volatility is below the GARCH forecast."}
              </p>

              <p style={{ fontSize: "0.7rem", color: "#64748b", marginTop: "0.75rem" }}>
                Expiry: {volComparison.iv_expiry} · Days to expiry: {volComparison.days_to_expiry}
              </p>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}

const buttonStyle = {
  width: "100%",
  marginTop: "0.5rem",
  background: "#0369a1",
  border: "none",
  borderRadius: "4px",
  color: "#e0f2fe",
  padding: "0.75rem",
  fontSize: "0.8rem",
  fontFamily: "inherit",
  letterSpacing: "0.1em",
  textTransform: "uppercase",
  cursor: "pointer",
}

const thStyle = {
  textAlign: "left",
  padding: "4px",
}

const tdStyle = {
  padding: "4px",
}

function Card({ title, children }) {
  return (
    <div style={{ background: "#0f172a", border: "1px solid #1e3a5f", borderRadius: "8px", padding: "1.5rem" }}>
      <p style={{ fontSize: "0.7rem", color: "#38bdf8", letterSpacing: "0.15em", textTransform: "uppercase", marginBottom: "1rem" }}>
        {title}
      </p>
      {children}
    </div>
  )
}

function Metric({ label, value, color = "#38bdf8", large = false }) {
  return (
    <div style={{ background: "#1e293b", borderRadius: "6px", padding: large ? "1rem" : "0.75rem" }}>
      <p style={{ fontSize: "0.6rem", color: "#64748b", marginBottom: "0.2rem", letterSpacing: "0.08em" }}>
        {label}
      </p>
      <p style={{ fontSize: large ? "1.4rem" : "0.95rem", color, fontWeight: large ? 700 : 600 }}>
        {value}
      </p>
    </div>
  )
}