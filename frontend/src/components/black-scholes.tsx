
const BlackScholes: React.FC = () => {

    return (
        <div className='flex h-screen w-screen   flex-col'>
            <div className="">
                <h1 className='text-white font-bold text-4xl mx-4 mt-20'>Black-Scholes Model Pricing</h1>
            </div>
            <div className='flex flex-row my-5'>
                <div className='mx-2 pr-2 pl-2'>   
                    <table className="min-w-full divide divide-gray-400">
                        <tbody className="bg-slate-900 divide divide-gray-400">
                            <tr>
                                <td className="table-labels">Delta(Δ):</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Vega(v):</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Gamma(Γ):</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Theta(Θ):</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Rho(ρ):</td>
                                <td className="table-values">?</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="mx-2 pr-2 pl-2">
                    <table className="min-w-full divide divide-gray-400">
                        <tbody className="bg-slate-900 divide divide-gray-400">
                            <tr>
                                <td className="table-labels">Risk Free Rate:</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Volatility:</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Underlying Price:</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Strike Price:</td>
                                <td className="table-values">?</td>
                            </tr>
                            <tr>
                                <td className="table-labels">Expiration:</td>
                                <td className="table-values">?</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="mx-2 px-14 pb-0 bg-gray-700 text-center rounded-md">
                    <h6 className="text-white text-xl underline mt-2">Analysis</h6>
                    <p className="text-white">Based on the Black Scholes model the option is (over/under) valued by xxx</p>
                </div>    
            </div>
            <div className='flex flex-row mx-2 justify-center'>
                <div className='bg-gray-700 text-center py-2 px-16 m-4 rounded-md'>
                    <h6 className="text-white text-lg mb-2">Bid Price</h6>
                    <p className="bold">?</p>
                </div>
                <div className='bg-gray-700 text-center py-2 px-16 m-4 rounded-md'>
                    <h6 className="text-white text-lg mb-2">Ask Price</h6>
                    <p className="bold">?</p>
                </div>
            </div>
        </div>
    )
}

export default BlackScholes;