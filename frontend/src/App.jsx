import { useState } from "react"

export default function App() {
    // declare your 6 state variables here

    const [stockPrice, setStockPrice] = useState(100)
    const [strikePrice, setStrikePrice] = useState(100)
    const [vol, setVol] = useState(0.2)
    const [rfr, setRfr] = useState(0.05)
    const [timeToExpiry, setTimeToExpiry] = useState(1)
    const [numSimulations, setNumSimulations] = useState(10000)
    const [priceResult, setPriceResult] = useState(null)
    const [greeksResult, setGreeksResult] = useState(null)


    const handleSubmit = async () => {

      const priceResponse = await fetch("http://127.0.0.1:8000/price", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({stockPrice, strikePrice, vol, rfr, timeToExpiry, numSimulations})
      
      })
      const priceData = await priceResponse.json()
      setPriceResult(priceData)
      const greekResponse = await fetch("http://127.0.0.1:8000/greeks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({stockPrice, strikePrice, vol, rfr, timeToExpiry, numSimulations})
      
      })
      const greekData = await greekResponse.json()
      setGreeksResult(greekData)
    }
    return (
        <div>

          <label htmlFor="stockPrice">Stock Price</label>
            <input 
                id="stockPrice"
                type="number"
                value={stockPrice}
                onChange={(e) => setStockPrice(Number(e.target.value))}
            />

          <label htmlFor="strikePrice">Strike Price</label>
            <input 
                id = "strikePrice"
                type="number"
                value={strikePrice}
                onChange={(e) => setStrikePrice(Number(e.target.value))}
            />

          <label htmlFor="vol">Volatility</label>
          <input 
              id = "vol"
              type="number"
              value={vol}
              step={0.01}
              onChange={(e) => setVol(Number(e.target.value))}
          />

          <label htmlFor="rfr">Risk Free Rate</label>
          <input 
              id = "rfr"
              type="number"
              value={rfr}
              step={0.01}
              onChange={(e) => setRfr(Number(e.target.value))}
          />

          <label htmlFor="TimeToExpiry">Time to Expiration</label>
          <input 
              id = "TimeToExpiry"
              type="number"
              value={timeToExpiry}
              step={0.01}
              onChange={(e) => setTimeToExpiry(Number(e.target.value))}
          />

          <label htmlFor="numSimulations">Number of Simulations</label>
          <input 
              id = "numSimulations"
              type="number"
              value={numSimulations}
              onChange={(e) => setNumSimulations(Number(e.target.value))}
          />

          <button onClick={handleSubmit}>Calculate</button>

          {priceResult && (

            <div>
              <p>Call Price: {priceResult["Call Price"]}</p>
              <p>Put Price: {priceResult["Put Price"]}</p>
              
            </div>
            )
          }
          {greeksResult && (
            <div>

              <p>Delta Call: {greeksResult["Delta Call"]}</p>
              <p>Delta Put: {greeksResult["Delta Put"]}</p>
              <p>Gamma: {greeksResult["Gamma Value"]}</p>
              <p>Vega: {greeksResult["Vega Value"]}</p>
              <p>Theta Call: {greeksResult["Theta Call"]}</p>
              <p>Theta Put: {greeksResult["Theta Put"]}</p>
              <p>Rho Call: {greeksResult["Rho Call"]}</p>
              <p>Rho Put: {greeksResult["Rho Put"]}</p>
              <p>Vanna: {greeksResult["Vanna Value"]}</p>
              <p>Volga: {greeksResult["Volga Value"]}</p>
              <p>Zomma: {greeksResult["Zomma Value"]}</p>
        
            </div>
          )}

        </div>
    )
}